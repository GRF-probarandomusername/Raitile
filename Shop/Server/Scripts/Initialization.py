""" Initialization"""
# Imports
from pathlib import Path
from datetime import datetime
import subprocess
import shutil
import time
import sys
import os
import ssl

if __package__:
    from .Error_Codes import ErrorCode, ServerError
else:
    from Error_Codes import ErrorCode, ServerError

# Paths and configuration
parent_dir = Path(__file__).resolve().parent.parent
public_folders = ["Public", "assets"]
private_folders = ["Config", "logs", "database", "Stock", "certs"]
required_certs = ["ca.crt", "server.crt", "server.key"]
today_date = datetime.today().strftime("%Y-%m-%d")
logs_file_name_and_location = parent_dir / "logs" / f"logs_{today_date}.txt"
# Temporarily disable log and crash-log file writes.
FILE_LOGGING_ENABLED = False  # Python logging is temporary: since the main thread will be run by a Go application, this variable stops Python from writing logs to avoid file corruption. Eventually, Python won't log at all.
init_stack_trace = ["------------------------------- Begin Stack Trace -----------------------------------------\n"]

# Terminal colors
RESET = "\033[0m"
ORANGE = "\033[38;5;208m"
YELLOW = "\033[93m"
RED = "\033[91m"
GREEN = "\033[92m"

# Helpers
def bip_error():
    if shutil.which("aplay") is None:
        return False
    bip = (b'\x00' * 10 + b'\xff' * 10) * 80
    end_time = time.time() + 5

    while time.time() < end_time:
        cycle_start = time.time()
        subprocess.run(
            ["aplay", "-q"],
            input=bip,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        
        pause = 0.8 - (time.time() - cycle_start)
        if pause > 0:
            time.sleep(pause)
    return True


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def next_crash_log_path():
    crash_log_id = 1
    while True:
        candidate = parent_dir / "logs" / f"crash_logs_{today_date}_{crash_log_id}.txt"
        if not candidate.exists():
            return candidate
        crash_log_id += 1


# Select the next available crash log path.
Stack_trace_location = next_crash_log_path()


def writing_stack_trace(crash):
    if not FILE_LOGGING_ENABLED:
        return
    if crash == True:
        with open(Stack_trace_location, "a", encoding="utf-8") as f:
            f.write("".join(init_stack_trace))
        with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
            f.write("".join(init_stack_trace))
    else:
        with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
            f.write("".join(init_stack_trace))


# Verify the authenticity of the certificates.
def verify_certificates():
    ca_cert_path = parent_dir / "certs" / "ca.crt"
    server_cert_path = parent_dir / "certs" / "server.crt"
    server_key_path = parent_dir / "certs" / "server.key"
    for certificate_path in (ca_cert_path, server_cert_path, server_key_path):
        if not certificate_path.is_file():
            code = (
                ErrorCode.PRIVATE_KEY_MISSING
                if certificate_path == server_key_path
                else ErrorCode.CERTIFICATE_MISSING
            )
            raise ServerError(code, f"Missing required file: {certificate_path}")

    # Loading the pair fails if the private key does not match the certificate.
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    try:
        ssl_context.load_cert_chain(
            certfile=str(server_cert_path),
            keyfile=str(server_key_path),
        )
    except ssl.SSLError as error:
        code = (
            ErrorCode.CERTIFICATE_KEY_MISMATCH
            if getattr(error, "reason", "") == "KEY_VALUES_MISMATCH"
            else ErrorCode.TLS_INITIALIZATION_FAILED
        )
        raise ServerError(
            code,
            f"Could not load the server certificate and private key: {error}",
        ) from error

    # Mutual TLS uses this certificate for both server and client authentication.
    for purpose in ("sslserver", "sslclient"):
        try:
            result = subprocess.run(
                [
                    "openssl", "verify", "-purpose", purpose,
                    "-CAfile", str(ca_cert_path), str(server_cert_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError as error:
            raise ServerError(
                ErrorCode.OPENSSL_NOT_FOUND,
                "OpenSSL is required to verify the server certificate.",
            ) from error

        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip()
            raise ServerError(
                ErrorCode.CERTIFICATE_CHAIN_INVALID,
                f"Certificate verification for {purpose} failed: {detail}",
            )

    return True


# Main execution
def run_initialization() -> bool:
    """Initialize the server and return whether it is ready to run."""
    global Stack_trace_location
    Stack_trace_location = next_crash_log_path()
    init_stack_trace.clear()
    init_stack_trace.append(
        "------------------------------- Begin Stack Trace -----------------------------------------\n"
    )

    try:
        init_stack_trace.append(
            f"[{ErrorCode.INITIALIZATION_STARTED.value}] [{now()}] Initialization started.\n"
        )
        # Creating folders & permissions
        for folder in public_folders:
            folder_path = parent_dir / folder
            folder_already_exists = folder_path.is_dir()
            try:
                folder_path.mkdir(exist_ok=True, parents=True)
            except PermissionError as error:
                raise ServerError(
                    ErrorCode.FOLDER_PERMISSION_DENIED,
                    f"Permission denied while creating {folder_path}: {error}",
                ) from error
            except OSError as error:
                raise ServerError(
                    ErrorCode.FOLDER_CREATION_FAILED,
                    f"Could not create {folder_path}: {error}",
                ) from error
            if folder_already_exists:
                warning = (
                    f"[{ErrorCode.FOLDER_ALREADY_EXISTS.value}] [{now()}] "
                    f"WARNING: Public folder already exists: {folder}\n"
                )
                print(f"{ORANGE}{warning.rstrip()}{RESET}")
                init_stack_trace.append(warning)
            else:
                init_stack_trace.append(
                    f"[{ErrorCode.FOLDER_CREATED.value}] [{now()}] "
                    f"Created public folder: {folder}\n"
                )

        for folder in private_folders:
            folder_path = parent_dir / folder
            folder_already_exists = folder_path.is_dir()
            try:
                folder_path.mkdir(exist_ok=True, parents=True)
            except PermissionError as error:
                raise ServerError(
                    ErrorCode.FOLDER_PERMISSION_DENIED,
                    f"Permission denied while creating {folder_path}: {error}",
                ) from error
            except OSError as error:
                raise ServerError(
                    ErrorCode.FOLDER_CREATION_FAILED,
                    f"Could not create {folder_path}: {error}",
                ) from error
            if folder_already_exists:
                warning = (
                    f"[{ErrorCode.FOLDER_ALREADY_EXISTS.value}] [{now()}] "
                    f"WARNING: Private folder already exists: {folder}\n"
                )
                print(f"{ORANGE}{warning.rstrip()}{RESET}")
                init_stack_trace.append(warning)
            else:
                init_stack_trace.append(
                    f"[{ErrorCode.FOLDER_CREATED.value}] [{now()}] "
                    f"Created private folder: {folder}\n"
                )
            if os.name != "nt":
                try:
                    os.chmod(folder_path, 0o700)
                except OSError as error:
                    raise ServerError(
                        ErrorCode.PERMISSION_CHANGE_FAILED,
                        f"Could not set permissions for {folder_path}: {error}",
                    ) from error

        # Checking certificates
        certs_dir = parent_dir / "certs"
        for cert in required_certs:
            if not (certs_dir / cert).is_file():
                code = (
                    ErrorCode.PRIVATE_KEY_MISSING
                    if cert == "server.key"
                    else ErrorCode.CERTIFICATE_MISSING
                )
                raise ServerError(
                    code,
                    f"Missing required security file: {cert} in {certs_dir}",
                )

        if os.name != "nt":
            try:
                os.chmod(certs_dir / "server.key", 0o600)
            except OSError as error:
                raise ServerError(
                    ErrorCode.PERMISSION_CHANGE_FAILED,
                    f"Could not secure the server private key: {error}",
                ) from error

        try:
            verify_certificates()
        except ServerError as certificate_error:
            init_stack_trace.append(f"[{now()}] {certificate_error}\n")
            raise
        init_stack_trace.append(
            f"[{ErrorCode.CERTIFICATES_VERIFIED.value}] [{now()}] "
            "Security certificates verified successfully.\n"
        )

        if FILE_LOGGING_ENABLED:
            try:
                with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
                    f.write(f"[{now()}] Initialization completed.\n")
            except OSError as error:
                raise ServerError(
                    ErrorCode.LOG_WRITE_FAILED,
                    f"Could not write to {logs_file_name_and_location}: {error}",
                ) from error
        init_stack_trace.append(
            f"[{ErrorCode.INITIALIZATION_COMPLETED.value}] [{now()}] "
            "Initialization completed.\n"
        )
    except Exception as e:
        if isinstance(e, ServerError):
            error_message = str(e)
        else:
            error_message = f"[{ErrorCode.INITIALIZATION_FAILED.value}] {e}"
        print(f"{RED}[{now()}] Initialization error: {error_message}{RESET}")
        init_stack_trace.append(f"[{now()}] Initialization error: {error_message}\n")
        try:
            if bip_error():
                init_stack_trace.append(f"[{now()}] Audio notification sent.\n")
            else:
                warning = (
                    f"[{ErrorCode.AUDIO_NOTIFICATION_FAILED.value}] [{now()}] "
                    "WARNING: Audio notification unavailable (aplay not found).\n"
                )
                print(f"{ORANGE}{warning.rstrip()}{RESET}")
                init_stack_trace.append(warning)
        except Exception as audio_error:
            warning = (
                f"[{ErrorCode.AUDIO_NOTIFICATION_FAILED.value}] [{now()}] "
                f"WARNING: Audio notification failed: {audio_error}\n"
            )
            print(f"{ORANGE}{warning.rstrip()}{RESET}")
            init_stack_trace.append(warning)
            if FILE_LOGGING_ENABLED:
                try:
                    with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
                        f.write(warning)
                except OSError as log_error:
                    print(
                        f"{ORANGE}[{ErrorCode.LOG_WRITE_FAILED.value}] "
                        f"WARNING: Could not write warning to log: {log_error}{RESET}"
                    )

        if FILE_LOGGING_ENABLED:
            try:
                with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
                    f.write(f"[{now()}] {error_message}\n")
            except OSError as log_error:
                print(
                    f"{ORANGE}[{ErrorCode.LOG_WRITE_FAILED.value}] "
                    f"Could not write initialization error to log: {log_error}{RESET}"
                )
        init_stack_trace.append(f"[{now()}] Exiting with status code 1.\n")
        init_stack_trace.append("--------------------------------- Ending Stack Trace ------------------------------\n")
        try:
            writing_stack_trace(crash=True)
        except OSError as log_error:
            print(
                f"{ORANGE}[{ErrorCode.STACK_TRACE_WRITE_FAILED.value}] "
                f"Could not write crash stack trace: {log_error}{RESET}"
            )
        print(f"{RED}[{now()}] Exiting with status code 1{RESET}")
        print(f"{YELLOW}[{now()}] Stack trace(the most important part) :{RESET}")
        print(f"{YELLOW}{''.join(init_stack_trace)}{RESET}")
        return False

    else:
        print(
            f"{GREEN}[{ErrorCode.INITIALIZATION_COMPLETED.value}] [{now()}] "
            f"Successfully initialized Raitile Shop (Server Side){RESET}"
        )
        init_stack_trace.append(f"------------------------------ Initialization Trace Ended ----------------------------------\n")
        try:
            writing_stack_trace(crash=False)
        except OSError as log_error:
            print(
                f"{RED}[{ErrorCode.STACK_TRACE_WRITE_FAILED.value}] "
                f"Could not write initialization stack trace: {log_error}{RESET}"
            )
            return False
        return True


if __name__ == "__main__":
    sys.exit(0 if run_initialization() else 1)
