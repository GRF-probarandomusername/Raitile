"""Machine-readable Raitile server error, warning, and information codes."""

from dataclasses import dataclass
from enum import Enum


class Severity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class ErrorCode(str, Enum):
    INITIALIZATION_FAILED = "R1001"
    FOLDER_CREATION_FAILED = "R1002"
    FOLDER_PERMISSION_DENIED = "R1003"
    REQUIRED_FOLDER_MISSING = "R1004"
    CONFIGURATION_MISSING = "R1005"
    CONFIGURATION_INVALID = "R1006"
    INITIALIZATION_TIMEOUT = "R1007"
    INITIALIZATION_INTERRUPTED = "R1008"

    CERTIFICATE_MISSING = "R1101"
    CERTIFICATE_INVALID = "R1102"
    CERTIFICATE_EXPIRED = "R1103"
    CERTIFICATE_NOT_YET_VALID = "R1104"
    CERTIFICATE_UNTRUSTED = "R1105"
    CERTIFICATE_AUTHORITY_INVALID = "R1106"
    CERTIFICATE_CHAIN_INVALID = "R1107"
    PRIVATE_KEY_MISSING = "R1108"
    PRIVATE_KEY_INVALID = "R1109"
    PRIVATE_KEY_PERMISSION_DENIED = "R1110"
    CERTIFICATE_KEY_MISMATCH = "R1111"
    OPENSSL_NOT_FOUND = "R1112"
    TLS_INITIALIZATION_FAILED = "R1113"

    FILE_NOT_FOUND = "R1201"
    FILE_READ_FAILED = "R1202"
    FILE_WRITE_FAILED = "R1203"
    FILE_CORRUPTED = "R1204"
    FILE_ALREADY_EXISTS = "R1205"
    DIRECTORY_NOT_FOUND = "R1206"
    DIRECTORY_CREATION_FAILED = "R1207"
    DIRECTORY_ACCESS_DENIED = "R1208"
    DISK_SPACE_EXHAUSTED = "R1209"
    PERMISSION_CHANGE_FAILED = "R1210"

    NETWORK_INITIALIZATION_FAILED = "R1301"
    PORT_ALREADY_IN_USE = "R1302"
    PORT_ACCESS_DENIED = "R1303"
    CONNECTION_REFUSED = "R1304"
    CONNECTION_TIMEOUT = "R1305"
    CONNECTION_LOST = "R1306"
    DNS_RESOLUTION_FAILED = "R1307"
    TLS_HANDSHAKE_FAILED = "R1308"
    INVALID_REQUEST = "R1309"
    TOO_MANY_CONNECTIONS = "R1310"

    DATABASE_NOT_FOUND = "R1401"
    DATABASE_CONNECTION_FAILED = "R1402"
    DATABASE_CORRUPTED = "R1403"
    DATABASE_ACCESS_DENIED = "R1404"
    DATABASE_QUERY_FAILED = "R1405"
    DATABASE_INITIALIZATION_FAILED = "R1406"
    DATABASE_LOCKED = "R1407"
    DATABASE_FULL = "R1408"
    DATABASE_MIGRATION_FAILED = "R1409"

    LOG_DIRECTORY_UNAVAILABLE = "R1501"
    LOG_FILE_CREATION_FAILED = "R1502"
    LOG_WRITE_FAILED = "R1503"
    LOG_READ_FAILED = "R1504"
    CRASH_LOG_CREATION_FAILED = "R1505"
    STACK_TRACE_WRITE_FAILED = "R1506"
    STACK_TRACE_GENERATION_FAILED = "R1507"
    LOG_PERMISSION_DENIED = "R1508"

    MEMORY_ALLOCATION_FAILED = "R1601"
    MEMORY_LIMIT_REACHED = "R1602"
    CPU_OVERLOAD = "R1603"
    PROCESS_CREATION_FAILED = "R1604"
    PROCESS_EXECUTION_FAILED = "R1605"
    DEPENDENCY_MISSING = "R1606"
    DEPENDENCY_VERSION_MISMATCH = "R1607"
    SYSTEM_RESOURCE_UNAVAILABLE = "R1608"

    SERVER_START_FAILED = "R1701"
    SERVER_STOP_FAILED = "R1702"
    SERVER_UNEXPECTED_SHUTDOWN = "R1703"
    SERVER_CRASH = "R1704"
    SERVER_ALREADY_RUNNING = "R1705"
    SERVER_NOT_RUNNING = "R1706"
    SERVER_UNRESPONSIVE = "R1707"
    SERVER_CONFIGURATION_ERROR = "R1708"

    FOLDER_ALREADY_EXISTS = "W1001"
    CERTIFICATE_EXPIRING_SOON = "W1002"
    LOW_DISK_SPACE = "W1003"
    HIGH_MEMORY_USAGE = "W1004"
    HIGH_CPU_USAGE = "W1005"
    OPENSSL_UNAVAILABLE = "W1006"
    AUDIO_NOTIFICATION_FAILED = "W1007"
    LOG_ROTATION_REQUIRED = "W1008"
    CONFIGURATION_DEFAULT_USED = "W1009"
    NON_CRITICAL_DEPENDENCY_MISSING = "W1010"
    NO_SERVER_KNOWN = "W1011"
    NO_USERS_KNOWN = "W1012"

    INITIALIZATION_STARTED = "I1001"
    INITIALIZATION_COMPLETED = "I1002"
    FOLDER_CREATED = "I1003"
    CERTIFICATES_VERIFIED = "I1004"
    DATABASE_CONNECTED = "I1005"
    SERVER_STARTED = "I1006"
    SERVER_STOPPED = "I1007"
    CONNECTION_ESTABLISHED = "I1008"
    CONNECTION_CLOSED = "I1009"
    CRASH_LOG_CREATED = "I1010"


@dataclass(frozen=True)
class ErrorCodeInfo:
    name: str
    description: str
    severity: Severity


ERROR_CODE_INFO: dict[ErrorCode, ErrorCodeInfo] = {
    ErrorCode.INITIALIZATION_FAILED: ErrorCodeInfo("INITIALIZATION_FAILED", "General server initialization failure.", Severity.ERROR),
    ErrorCode.FOLDER_CREATION_FAILED: ErrorCodeInfo("FOLDER_CREATION_FAILED", "Failed to create a required folder.", Severity.ERROR),
    ErrorCode.FOLDER_PERMISSION_DENIED: ErrorCodeInfo("FOLDER_PERMISSION_DENIED", "Insufficient permissions to access a folder.", Severity.ERROR),
    ErrorCode.REQUIRED_FOLDER_MISSING: ErrorCodeInfo("REQUIRED_FOLDER_MISSING", "A required folder is missing.", Severity.ERROR),
    ErrorCode.CONFIGURATION_MISSING: ErrorCodeInfo("CONFIGURATION_MISSING", "Configuration file not found.", Severity.ERROR),
    ErrorCode.CONFIGURATION_INVALID: ErrorCodeInfo("CONFIGURATION_INVALID", "Configuration file is invalid or malformed.", Severity.ERROR),
    ErrorCode.INITIALIZATION_TIMEOUT: ErrorCodeInfo("INITIALIZATION_TIMEOUT", "Initialization exceeded the allowed time limit.", Severity.ERROR),
    ErrorCode.INITIALIZATION_INTERRUPTED: ErrorCodeInfo("INITIALIZATION_INTERRUPTED", "Initialization was interrupted.", Severity.ERROR),
    ErrorCode.CERTIFICATE_MISSING: ErrorCodeInfo("CERTIFICATE_MISSING", "A required certificate is missing.", Severity.ERROR),
    ErrorCode.CERTIFICATE_INVALID: ErrorCodeInfo("CERTIFICATE_INVALID", "Certificate is invalid or unreadable.", Severity.ERROR),
    ErrorCode.CERTIFICATE_EXPIRED: ErrorCodeInfo("CERTIFICATE_EXPIRED", "Certificate has expired.", Severity.ERROR),
    ErrorCode.CERTIFICATE_NOT_YET_VALID: ErrorCodeInfo("CERTIFICATE_NOT_YET_VALID", "Certificate is not yet valid.", Severity.ERROR),
    ErrorCode.CERTIFICATE_UNTRUSTED: ErrorCodeInfo("CERTIFICATE_UNTRUSTED", "Certificate is not trusted.", Severity.ERROR),
    ErrorCode.CERTIFICATE_AUTHORITY_INVALID: ErrorCodeInfo("CERTIFICATE_AUTHORITY_INVALID", "Certificate authority is invalid.", Severity.ERROR),
    ErrorCode.CERTIFICATE_CHAIN_INVALID: ErrorCodeInfo("CERTIFICATE_CHAIN_INVALID", "Certificate chain is invalid.", Severity.ERROR),
    ErrorCode.PRIVATE_KEY_MISSING: ErrorCodeInfo("PRIVATE_KEY_MISSING", "Private key is missing.", Severity.ERROR),
    ErrorCode.PRIVATE_KEY_INVALID: ErrorCodeInfo("PRIVATE_KEY_INVALID", "Private key is invalid or unreadable.", Severity.ERROR),
    ErrorCode.PRIVATE_KEY_PERMISSION_DENIED: ErrorCodeInfo("PRIVATE_KEY_PERMISSION_DENIED", "Insufficient permissions to access the private key.", Severity.ERROR),
    ErrorCode.CERTIFICATE_KEY_MISMATCH: ErrorCodeInfo("CERTIFICATE_KEY_MISMATCH", "Certificate and private key do not match.", Severity.ERROR),
    ErrorCode.OPENSSL_NOT_FOUND: ErrorCodeInfo("OPENSSL_NOT_FOUND", "OpenSSL executable was not found on the system.", Severity.ERROR),
    ErrorCode.TLS_INITIALIZATION_FAILED: ErrorCodeInfo("TLS_INITIALIZATION_FAILED", "Failed to initialize the TLS context.", Severity.ERROR),
    ErrorCode.FILE_NOT_FOUND: ErrorCodeInfo("FILE_NOT_FOUND", "Required file not found.", Severity.ERROR),
    ErrorCode.FILE_READ_FAILED: ErrorCodeInfo("FILE_READ_FAILED", "Failed to read a file.", Severity.ERROR),
    ErrorCode.FILE_WRITE_FAILED: ErrorCodeInfo("FILE_WRITE_FAILED", "Failed to write to a file.", Severity.ERROR),
    ErrorCode.FILE_CORRUPTED: ErrorCodeInfo("FILE_CORRUPTED", "File is corrupted or unusable.", Severity.ERROR),
    ErrorCode.FILE_ALREADY_EXISTS: ErrorCodeInfo("FILE_ALREADY_EXISTS", "A file with the same name already exists.", Severity.ERROR),
    ErrorCode.DIRECTORY_NOT_FOUND: ErrorCodeInfo("DIRECTORY_NOT_FOUND", "Directory not found.", Severity.ERROR),
    ErrorCode.DIRECTORY_CREATION_FAILED: ErrorCodeInfo("DIRECTORY_CREATION_FAILED", "Failed to create a directory.", Severity.ERROR),
    ErrorCode.DIRECTORY_ACCESS_DENIED: ErrorCodeInfo("DIRECTORY_ACCESS_DENIED", "Access to the directory was denied.", Severity.ERROR),
    ErrorCode.DISK_SPACE_EXHAUSTED: ErrorCodeInfo("DISK_SPACE_EXHAUSTED", "Insufficient disk space.", Severity.ERROR),
    ErrorCode.PERMISSION_CHANGE_FAILED: ErrorCodeInfo("PERMISSION_CHANGE_FAILED", "Failed to change permissions.", Severity.ERROR),
    ErrorCode.NETWORK_INITIALIZATION_FAILED: ErrorCodeInfo("NETWORK_INITIALIZATION_FAILED", "Failed to initialize the network.", Severity.ERROR),
    ErrorCode.PORT_ALREADY_IN_USE: ErrorCodeInfo("PORT_ALREADY_IN_USE", "Requested port is already in use.", Severity.ERROR),
    ErrorCode.PORT_ACCESS_DENIED: ErrorCodeInfo("PORT_ACCESS_DENIED", "Insufficient permissions to use the port.", Severity.ERROR),
    ErrorCode.CONNECTION_REFUSED: ErrorCodeInfo("CONNECTION_REFUSED", "Connection was refused by the remote server.", Severity.ERROR),
    ErrorCode.CONNECTION_TIMEOUT: ErrorCodeInfo("CONNECTION_TIMEOUT", "Connection timed out.", Severity.ERROR),
    ErrorCode.CONNECTION_LOST: ErrorCodeInfo("CONNECTION_LOST", "Connection was lost.", Severity.ERROR),
    ErrorCode.DNS_RESOLUTION_FAILED: ErrorCodeInfo("DNS_RESOLUTION_FAILED", "Failed to resolve the domain name.", Severity.ERROR),
    ErrorCode.TLS_HANDSHAKE_FAILED: ErrorCodeInfo("TLS_HANDSHAKE_FAILED", "TLS handshake failed.", Severity.ERROR),
    ErrorCode.INVALID_REQUEST: ErrorCodeInfo("INVALID_REQUEST", "Network request is invalid.", Severity.ERROR),
    ErrorCode.TOO_MANY_CONNECTIONS: ErrorCodeInfo("TOO_MANY_CONNECTIONS", "Maximum number of connections reached.", Severity.ERROR),
    ErrorCode.DATABASE_NOT_FOUND: ErrorCodeInfo("DATABASE_NOT_FOUND", "Database not found.", Severity.ERROR),
    ErrorCode.DATABASE_CONNECTION_FAILED: ErrorCodeInfo("DATABASE_CONNECTION_FAILED", "Failed to connect to the database.", Severity.ERROR),
    ErrorCode.DATABASE_CORRUPTED: ErrorCodeInfo("DATABASE_CORRUPTED", "Database is corrupted.", Severity.ERROR),
    ErrorCode.DATABASE_ACCESS_DENIED: ErrorCodeInfo("DATABASE_ACCESS_DENIED", "Access to the database was denied.", Severity.ERROR),
    ErrorCode.DATABASE_QUERY_FAILED: ErrorCodeInfo("DATABASE_QUERY_FAILED", "Query execution failed.", Severity.ERROR),
    ErrorCode.DATABASE_INITIALIZATION_FAILED: ErrorCodeInfo("DATABASE_INITIALIZATION_FAILED", "Failed to initialize the database.", Severity.ERROR),
    ErrorCode.DATABASE_LOCKED: ErrorCodeInfo("DATABASE_LOCKED", "Database is locked.", Severity.ERROR),
    ErrorCode.DATABASE_FULL: ErrorCodeInfo("DATABASE_FULL", "Database is full.", Severity.ERROR),
    ErrorCode.DATABASE_MIGRATION_FAILED: ErrorCodeInfo("DATABASE_MIGRATION_FAILED", "Database migration failed.", Severity.ERROR),
    ErrorCode.LOG_DIRECTORY_UNAVAILABLE: ErrorCodeInfo("LOG_DIRECTORY_UNAVAILABLE", "Log directory is unavailable.", Severity.ERROR),
    ErrorCode.LOG_FILE_CREATION_FAILED: ErrorCodeInfo("LOG_FILE_CREATION_FAILED", "Failed to create a log file.", Severity.ERROR),
    ErrorCode.LOG_WRITE_FAILED: ErrorCodeInfo("LOG_WRITE_FAILED", "Failed to write to the logs.", Severity.ERROR),
    ErrorCode.LOG_READ_FAILED: ErrorCodeInfo("LOG_READ_FAILED", "Failed to read the logs.", Severity.ERROR),
    ErrorCode.CRASH_LOG_CREATION_FAILED: ErrorCodeInfo("CRASH_LOG_CREATION_FAILED", "Failed to create a crash log.", Severity.ERROR),
    ErrorCode.STACK_TRACE_WRITE_FAILED: ErrorCodeInfo("STACK_TRACE_WRITE_FAILED", "Failed to write the stack trace.", Severity.ERROR),
    ErrorCode.STACK_TRACE_GENERATION_FAILED: ErrorCodeInfo("STACK_TRACE_GENERATION_FAILED", "Failed to generate the stack trace.", Severity.ERROR),
    ErrorCode.LOG_PERMISSION_DENIED: ErrorCodeInfo("LOG_PERMISSION_DENIED", "Insufficient permissions to access the logs.", Severity.ERROR),
    ErrorCode.MEMORY_ALLOCATION_FAILED: ErrorCodeInfo("MEMORY_ALLOCATION_FAILED", "Failed to allocate memory.", Severity.ERROR),
    ErrorCode.MEMORY_LIMIT_REACHED: ErrorCodeInfo("MEMORY_LIMIT_REACHED", "Memory limit reached.", Severity.ERROR),
    ErrorCode.CPU_OVERLOAD: ErrorCodeInfo("CPU_OVERLOAD", "CPU load is unusually high.", Severity.ERROR),
    ErrorCode.PROCESS_CREATION_FAILED: ErrorCodeInfo("PROCESS_CREATION_FAILED", "Failed to create a process.", Severity.ERROR),
    ErrorCode.PROCESS_EXECUTION_FAILED: ErrorCodeInfo("PROCESS_EXECUTION_FAILED", "Process execution failed.", Severity.ERROR),
    ErrorCode.DEPENDENCY_MISSING: ErrorCodeInfo("DEPENDENCY_MISSING", "A required dependency is missing.", Severity.ERROR),
    ErrorCode.DEPENDENCY_VERSION_MISMATCH: ErrorCodeInfo("DEPENDENCY_VERSION_MISMATCH", "Dependency version is incompatible.", Severity.ERROR),
    ErrorCode.SYSTEM_RESOURCE_UNAVAILABLE: ErrorCodeInfo("SYSTEM_RESOURCE_UNAVAILABLE", "A system resource is unavailable.", Severity.ERROR),
    ErrorCode.SERVER_START_FAILED: ErrorCodeInfo("SERVER_START_FAILED", "Failed to start the server.", Severity.ERROR),
    ErrorCode.SERVER_STOP_FAILED: ErrorCodeInfo("SERVER_STOP_FAILED", "Failed to stop the server cleanly.", Severity.ERROR),
    ErrorCode.SERVER_UNEXPECTED_SHUTDOWN: ErrorCodeInfo("SERVER_UNEXPECTED_SHUTDOWN", "Server shut down unexpectedly.", Severity.ERROR),
    ErrorCode.SERVER_CRASH: ErrorCodeInfo("SERVER_CRASH", "The server crashed.", Severity.ERROR),
    ErrorCode.SERVER_ALREADY_RUNNING: ErrorCodeInfo("SERVER_ALREADY_RUNNING", "A server instance is already running.", Severity.ERROR),
    ErrorCode.SERVER_NOT_RUNNING: ErrorCodeInfo("SERVER_NOT_RUNNING", "The server is not running.", Severity.ERROR),
    ErrorCode.SERVER_UNRESPONSIVE: ErrorCodeInfo("SERVER_UNRESPONSIVE", "The server is not responding.", Severity.ERROR),
    ErrorCode.SERVER_CONFIGURATION_ERROR: ErrorCodeInfo("SERVER_CONFIGURATION_ERROR", "Server configuration is invalid.", Severity.ERROR),
    ErrorCode.FOLDER_ALREADY_EXISTS: ErrorCodeInfo("FOLDER_ALREADY_EXISTS", "A folder already exists.", Severity.WARNING),
    ErrorCode.CERTIFICATE_EXPIRING_SOON: ErrorCodeInfo("CERTIFICATE_EXPIRING_SOON", "A certificate will expire soon.", Severity.WARNING),
    ErrorCode.LOW_DISK_SPACE: ErrorCodeInfo("LOW_DISK_SPACE", "Disk space is running low.", Severity.WARNING),
    ErrorCode.HIGH_MEMORY_USAGE: ErrorCodeInfo("HIGH_MEMORY_USAGE", "Memory usage is high.", Severity.WARNING),
    ErrorCode.HIGH_CPU_USAGE: ErrorCodeInfo("HIGH_CPU_USAGE", "CPU usage is high.", Severity.WARNING),
    ErrorCode.OPENSSL_UNAVAILABLE: ErrorCodeInfo("OPENSSL_UNAVAILABLE", "OpenSSL is unavailable for an operation that requires it.", Severity.WARNING),
    ErrorCode.AUDIO_NOTIFICATION_FAILED: ErrorCodeInfo("AUDIO_NOTIFICATION_FAILED", "Failed to play the audio notification.", Severity.WARNING),
    ErrorCode.LOG_ROTATION_REQUIRED: ErrorCodeInfo("LOG_ROTATION_REQUIRED", "Log rotation is recommended.", Severity.WARNING),
    ErrorCode.CONFIGURATION_DEFAULT_USED: ErrorCodeInfo("CONFIGURATION_DEFAULT_USED", "A default configuration was used.", Severity.WARNING),
    ErrorCode.NON_CRITICAL_DEPENDENCY_MISSING: ErrorCodeInfo("NON_CRITICAL_DEPENDENCY_MISSING", "A non-critical dependency is missing.", Severity.WARNING),
    ErrorCode.INITIALIZATION_STARTED: ErrorCodeInfo("INITIALIZATION_STARTED", "Initialization started.", Severity.INFO),
    ErrorCode.INITIALIZATION_COMPLETED: ErrorCodeInfo("INITIALIZATION_COMPLETED", "Initialization completed.", Severity.INFO),
    ErrorCode.FOLDER_CREATED: ErrorCodeInfo("FOLDER_CREATED", "Folder created.", Severity.INFO),
    ErrorCode.CERTIFICATES_VERIFIED: ErrorCodeInfo("CERTIFICATES_VERIFIED", "Certificates verified.", Severity.INFO),
    ErrorCode.DATABASE_CONNECTED: ErrorCodeInfo("DATABASE_CONNECTED", "Database connection established.", Severity.INFO),
    ErrorCode.SERVER_STARTED: ErrorCodeInfo("SERVER_STARTED", "Server started.", Severity.INFO),
    ErrorCode.SERVER_STOPPED: ErrorCodeInfo("SERVER_STOPPED", "Server stopped.", Severity.INFO),
    ErrorCode.CONNECTION_ESTABLISHED: ErrorCodeInfo("CONNECTION_ESTABLISHED", "New connection established.", Severity.INFO),
    ErrorCode.CONNECTION_CLOSED: ErrorCodeInfo("CONNECTION_CLOSED", "Connection closed.", Severity.INFO),
    ErrorCode.CRASH_LOG_CREATED: ErrorCodeInfo("CRASH_LOG_CREATED", "Crash log created.", Severity.INFO),
}


class ServerError(Exception):
    def __init__(self, code: ErrorCode, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code.value}] {message}")


__all__ = ["ErrorCode", "ErrorCodeInfo", "ERROR_CODE_INFO", "ServerError", "Severity"]
