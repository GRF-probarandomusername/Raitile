"""Discover trusted peers over mutual TLS.

The configured CA must issue peer certificates valid for both TLS server and
client authentication. Registered peer names must match certificate names.
"""

from dataclasses import dataclass, field
from datetime import datetime
import errno
import ipaddress
import json
import math
from pathlib import Path
import shutil
import socket
import ssl
import struct
import subprocess
import threading
import time
from typing import Any

if __package__:
    from .Error_Codes import ErrorCode, ServerError
    from .Initialization import run_initialization
else:
    from Error_Codes import ErrorCode, ServerError
    from Initialization import run_initialization

parent_dir = Path(__file__).resolve().parent.parent
certs_dir = parent_dir / "certs"
known_users_file = parent_dir / "database" / "known_users.json"
known_servers_file = parent_dir / "database" / "known_servers.json"

DISCOVERY_HOST = "0.0.0.0"
DISCOVERY_PORT = 55555
MAX_MESSAGE_SIZE = 64 * 1024
MAX_REGISTRY_ENTRIES = 10_000
SYNC_INTERVAL_SECONDS = 15
CONNECTION_TIMEOUT_SECONDS = 3

RESET = "\033[0m"
ORANGE = "\033[38;5;208m"
YELLOW = "\033[93m"
RED = "\033[91m"
GREEN = "\033[92m"

Registry = dict[str, str]


@dataclass
class DiscoveryState:
    known_users: Registry
    known_servers: Registry
    lock: threading.RLock = field(default_factory=threading.RLock, repr=False)


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def console_log(color: str, message: str) -> None:
    print(f"{color}[{now()}] {message}{RESET}")


def play_discovery_error_beep() -> None:
    if shutil.which("aplay") is None:
        console_log(
            YELLOW,
            f"[{ErrorCode.AUDIO_NOTIFICATION_FAILED.value}] "
            "Discovery error sound is unavailable because aplay was not found.",
        )
        return

    sample_rate = 8000

    def tone(frequency: int, duration: float) -> bytes:
        sample_count = int(sample_rate * duration)
        return bytes(
            int(128 + 70 * math.sin(2 * math.pi * frequency * sample / sample_rate))
            for sample in range(sample_count)
        )

    sound = tone(880, 0.16) + bytes([128] * 800) + tone(660, 0.2)
    try:
        subprocess.run(
            ["aplay", "-q", "-t", "raw", "-f", "U8", "-r", str(sample_rate)],
            input=sound,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        console_log(
            YELLOW,
            f"[{ErrorCode.AUDIO_NOTIFICATION_FAILED.value}] "
            f"Could not play the discovery error sound: {error}",
        )


def get_local_ipv4() -> str:
    hostname = socket.gethostname()
    try:
        addresses = socket.getaddrinfo(hostname, None, socket.AF_INET, socket.SOCK_STREAM)
    except socket.gaierror as error:
        raise ServerError(
            ErrorCode.DNS_RESOLUTION_FAILED,
            f"Could not resolve the local hostname {hostname}: {error}",
        ) from error

    for address in addresses:
        ip_address = address[4][0]
        if not ipaddress.IPv4Address(ip_address).is_loopback:
            return ip_address
    return "127.0.0.1"


def validate_registry(value: Any) -> Registry:
    if not isinstance(value, dict) or len(value) > MAX_REGISTRY_ENTRIES:
        raise ServerError(ErrorCode.INVALID_REQUEST, "Registry must be a bounded JSON object.")

    registry: Registry = {}
    for name, address in value.items():
        if (
            not isinstance(name, str)
            or not name.strip()
            or len(name) > 255
            or not isinstance(address, str)
        ):
            raise ServerError(ErrorCode.INVALID_REQUEST, "Registry contains an invalid entry.")
        try:
            ipaddress.IPv4Address(address)
        except ipaddress.AddressValueError as error:
            raise ServerError(
                ErrorCode.INVALID_REQUEST,
                f"Registry contains an invalid IPv4 address for {name}.",
            ) from error
        registry[name] = address
    return registry


def load_registry(path: Path) -> Registry | None:
    if not path.is_file():
        return None

    try:
        with path.open("r", encoding="utf-8") as file:
            return validate_registry(json.load(file))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError, ServerError) as error:
        if isinstance(error, ServerError):
            raise
        raise ServerError(
            ErrorCode.FILE_CORRUPTED,
            f"Could not read a valid registry from {path}: {error}",
        ) from error


def save_registry(path: Path, registry: Registry) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as file:
            json.dump(registry, file, indent=4)
    except OSError as error:
        raise ServerError(
            ErrorCode.FILE_WRITE_FAILED,
            f"Could not write registry {path}: {error}",
        ) from error


def load_known_users() -> Registry:
    registry = load_registry(known_users_file)
    if registry is None:
        console_log(
            YELLOW,
            f"WARNING: Known users file not found at {known_users_file}; "
            "starting with an empty list.",
        )
        return {}
    return registry


def load_known_servers() -> Registry:
    registry = load_registry(known_servers_file)
    if registry is not None:
        return registry

    console_log(
        YELLOW,
        f"WARNING: Known servers file not found at {known_servers_file}; "
        "creating it with this server.",
    )
    registry = {socket.gethostname(): get_local_ipv4()}
    save_registry(known_servers_file, registry)
    return registry


def create_server_tls_context() -> ssl.SSLContext:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(
        certfile=str(certs_dir / "server.crt"),
        keyfile=str(certs_dir / "server.key"),
    )
    context.load_verify_locations(cafile=str(certs_dir / "ca.crt"))
    context.verify_mode = ssl.CERT_REQUIRED
    return context


def create_client_tls_context() -> ssl.SSLContext:
    context = ssl.create_default_context(
        ssl.Purpose.SERVER_AUTH,
        cafile=str(certs_dir / "ca.crt"),
    )
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.load_cert_chain(
        certfile=str(certs_dir / "server.crt"),
        keyfile=str(certs_dir / "server.key"),
    )
    return context


def receive_exact(connection: socket.socket, size: int) -> bytes | None:
    data = bytearray()
    while len(data) < size:
        chunk = connection.recv(size - len(data))
        if not chunk:
            if not data:
                return None
            raise ServerError(ErrorCode.INVALID_REQUEST, "Connection ended during a message.")
        data.extend(chunk)
    return bytes(data)


def receive_json(connection: socket.socket) -> dict[str, Any] | None:
    header = receive_exact(connection, 4)
    if header is None:
        return None

    message_size = struct.unpack("!I", header)[0]
    if message_size == 0 or message_size > MAX_MESSAGE_SIZE:
        raise ServerError(ErrorCode.INVALID_REQUEST, "Message size is invalid.")

    payload = receive_exact(connection, message_size)
    if payload is None:
        raise ServerError(ErrorCode.INVALID_REQUEST, "Message payload is missing.")
    try:
        message = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ServerError(ErrorCode.INVALID_REQUEST, "Message is not valid UTF-8 JSON.") from error
    if not isinstance(message, dict):
        raise ServerError(ErrorCode.INVALID_REQUEST, "Message must be a JSON object.")
    return message


def send_json(connection: socket.socket, message: dict[str, Any]) -> None:
    payload = json.dumps(message, separators=(",", ":")).encode("utf-8")
    if not payload or len(payload) > MAX_MESSAGE_SIZE:
        raise ServerError(ErrorCode.INVALID_REQUEST, "Response exceeds the message size limit.")
    connection.sendall(struct.pack("!I", len(payload)) + payload)


def handle_peer_message(
    connection: socket.socket,
    peer_address: tuple[str, int],
    state: DiscoveryState,
) -> None:
    message = receive_json(connection)
    if message is None:
        return

    action = message.get("action")
    name = message.get("name")
    if action not in {"REGISTER_USER", "REGISTER_SERVER"}:
        raise ServerError(ErrorCode.INVALID_REQUEST, "Unsupported discovery action.")
    if not isinstance(name, str) or not name.strip() or len(name) > 255:
        raise ServerError(ErrorCode.INVALID_REQUEST, "Peer name is missing or invalid.")

    certificate = connection.getpeercert()
    certificate_names = {
        value
        for kind, value in certificate.get("subjectAltName", ())
        if kind in {"DNS", "IP Address"}
    }
    certificate_names.update(
        value
        for relative_name in certificate.get("subject", ())
        for key, value in relative_name
        if key == "commonName"
    )
    if name not in certificate_names:
        raise ServerError(
            ErrorCode.INVALID_REQUEST,
            "Peer name does not match the authenticated certificate.",
        )

    peer_ip = peer_address[0]
    with state.lock:
        registry = state.known_users if action == "REGISTER_USER" else state.known_servers
        registry_path = known_users_file if action == "REGISTER_USER" else known_servers_file
        registry[name] = peer_ip
        save_registry(registry_path, registry)
        response = {
            "status": "OK",
            "servers": state.known_servers.copy(),
            "users": state.known_users.copy(),
        }
    send_json(connection, response)
    console_log(GREEN, f"Registered trusted peer {name} ({peer_ip}).")


def handle_peer_connection(
    raw_connection: socket.socket,
    peer_address: tuple[str, int],
    tls_context: ssl.SSLContext,
    state: DiscoveryState,
) -> None:
    try:
        with tls_context.wrap_socket(raw_connection, server_side=True) as connection:
            handle_peer_message(connection, peer_address, state)
    except ServerError as error:
        console_log(ORANGE, str(error))
    except ssl.SSLError as error:
        console_log(
            ORANGE,
            f"[{ErrorCode.TLS_HANDSHAKE_FAILED.value}] "
            f"Rejected an unauthenticated or invalid TLS peer: {error}",
        )
    except OSError as error:
        console_log(
            ORANGE,
            f"[{ErrorCode.CONNECTION_LOST.value}] "
            f"Peer connection {peer_address[0]} failed: {error}",
        )


def open_discovery_socket() -> socket.socket:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server_socket.bind((DISCOVERY_HOST, DISCOVERY_PORT))
        server_socket.listen(20)
        server_socket.settimeout(1.0)
    except OSError as error:
        server_socket.close()
        code = (
            ErrorCode.PORT_ALREADY_IN_USE
            if error.errno == errno.EADDRINUSE
            else ErrorCode.NETWORK_INITIALIZATION_FAILED
        )
        raise ServerError(code, f"Could not listen on port {DISCOVERY_PORT}: {error}") from error
    return server_socket


def listen_for_peers(
    server_socket: socket.socket,
    tls_context: ssl.SSLContext,
    state: DiscoveryState,
) -> None:
    console_log(GREEN, f"Listening for mutually authenticated peers on port {DISCOVERY_PORT}.")
    while True:
        try:
            connection, address = server_socket.accept()
        except socket.timeout:
            continue
        except OSError as error:
            console_log(
                RED,
                f"[{ErrorCode.NETWORK_INITIALIZATION_FAILED.value}] "
                f"Discovery listener stopped: {error}",
            )
            play_discovery_error_beep()
            return

        connection.settimeout(5.0)
        handle_peer_connection(connection, address, tls_context, state)


def sync_with_known_servers(
    client_context: ssl.SSLContext,
    state: DiscoveryState,
) -> None:
    hostname = socket.gethostname()
    last_error_beep_at = -30.0

    def beep_for_sync_error() -> None:
        nonlocal last_error_beep_at
        current_time = time.monotonic()
        if current_time - last_error_beep_at >= 30:
            play_discovery_error_beep()
            last_error_beep_at = current_time

    while True:
        with state.lock:
            peers = list(state.known_servers.items())

        for peer_name, peer_ip in peers:
            if peer_name == hostname or ipaddress.IPv4Address(peer_ip).is_loopback:
                continue

            try:
                with socket.create_connection(
                    (peer_ip, DISCOVERY_PORT),
                    timeout=CONNECTION_TIMEOUT_SECONDS,
                ) as raw_connection:
                    with client_context.wrap_socket(
                        raw_connection,
                        server_hostname=peer_name,
                    ) as connection:
                        send_json(
                            connection,
                            {"action": "REGISTER_SERVER", "name": hostname},
                        )
                        response = receive_json(connection)

                if response is None or response.get("status") != "OK":
                    raise ServerError(
                        ErrorCode.INVALID_REQUEST,
                        f"Peer {peer_name} returned an invalid response.",
                    )

                remote_servers = validate_registry(response.get("servers"))
                remote_users = validate_registry(response.get("users"))
                with state.lock:
                    servers_before = state.known_servers.copy()
                    users_before = state.known_users.copy()
                    state.known_servers.update(remote_servers)
                    state.known_servers[peer_name] = peer_ip
                    state.known_users.update(remote_users)
                    if state.known_servers != servers_before:
                        save_registry(known_servers_file, state.known_servers)
                        console_log(GREEN, f"Updated the server registry from {peer_name}.")
                    if state.known_users != users_before:
                        save_registry(known_users_file, state.known_users)
                        console_log(GREEN, f"Updated the user registry from {peer_name}.")
            except ServerError as error:
                console_log(ORANGE, str(error))
                beep_for_sync_error()
            except ssl.SSLError as error:
                console_log(
                    ORANGE,
                    f"[{ErrorCode.TLS_HANDSHAKE_FAILED.value}] "
                    f"TLS verification failed for {peer_name}: {error}",
                )
                beep_for_sync_error()
            except socket.timeout as error:
                console_log(
                    ORANGE,
                    f"[{ErrorCode.CONNECTION_TIMEOUT.value}] "
                    f"Connection to {peer_name} ({peer_ip}) timed out: {error}",
                )
                beep_for_sync_error()
            except ConnectionRefusedError as error:
                console_log(
                    ORANGE,
                    f"[{ErrorCode.CONNECTION_REFUSED.value}] "
                    f"Connection to {peer_name} ({peer_ip}) was refused: {error}",
                )
                beep_for_sync_error()
            except OSError as error:
                console_log(
                    ORANGE,
                    f"[{ErrorCode.CONNECTION_LOST.value}] "
                    f"Could not synchronize with {peer_name} ({peer_ip}): {error}",
                )
                beep_for_sync_error()

        time.sleep(SYNC_INTERVAL_SECONDS)


def run_server_discovery() -> bool:
    if not run_initialization():
        return False

    try:
        state = DiscoveryState(
            known_users=load_known_users(),
            known_servers=load_known_servers(),
        )
        server_context = create_server_tls_context()
        client_context = create_client_tls_context()
        server_socket = open_discovery_socket()
    except ServerError as error:
        console_log(RED, str(error))
        play_discovery_error_beep()
        return False
    except (OSError, ssl.SSLError) as error:
        server_error = ServerError(
            ErrorCode.TLS_INITIALIZATION_FAILED,
            f"Could not prepare mutual TLS discovery: {error}",
        )
        console_log(RED, str(server_error))
        play_discovery_error_beep()
        return False

    if not state.known_users:
        console_log(YELLOW, "No users are currently known.")
    if len(state.known_servers) <= 1:
        console_log(YELLOW, "No peer servers are currently known.")

    listener_thread = threading.Thread(
        target=listen_for_peers,
        args=(server_socket, server_context, state),
        daemon=True,
    )
    listener_thread.start()

    try:
        sync_with_known_servers(client_context, state)
    except KeyboardInterrupt:
        server_socket.close()
        print()
        console_log(YELLOW, "Server discovery stopped.")
    return True


if __name__ == "__main__":
    if not run_server_discovery():
        raise SystemExit(1)
