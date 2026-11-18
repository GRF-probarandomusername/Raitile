**Raitile Server Error Codes**  
This catalogue documents the codes used by the server. Codes are stable: never  
   
 reuse an identifier for a different meaning. Exception details (such as a file  
   
 path or OpenSSL output) can be included in the message without changing the code.  
The Python module at `Scripts/Error_Codes.py` exposes these codes through  
   
 `ErrorCode`, their descriptions and severity through `ERROR_CODE_INFO`, and the  
   
 `ServerError` exception.  
Run the initialization module from the `Shop` directory with:  
```  
python -m Server.Scripts.Initialization  
   
```  
Other server modules can import the codes with:  
```  
from Server.Scripts.Error_Codes import ErrorCode, ServerError  
   
```  
**Initialization (R1000–R1099)**  
  
|  |  |  |  
| - | - | - |  
| **Code** |  **Name** |  **Description** |  
| R1001 |  INITIALIZATION_FAILED |  General server initialization failure. |  
| R1002 |  FOLDER_CREATION_FAILED |  Failed to create a required folder. |  
| R1003 |  FOLDER_PERMISSION_DENIED |  Insufficient permissions to access a folder. |  
| R1004 |  REQUIRED_FOLDER_MISSING |  A required folder is missing. |  
| R1005 |  CONFIGURATION_MISSING |  Configuration file not found. |  
| R1006 |  CONFIGURATION_INVALID |  Configuration file is invalid or malformed. |  
| R1007 |  INITIALIZATION_TIMEOUT |  Initialization exceeded the allowed time limit. |  
| R1008 |  INITIALIZATION_INTERRUPTED |  Initialization was interrupted. |  
  
   
**Certificates and security (R1100–R1199)**  
  
|  |  |  |  
| - | - | - |  
| **Code** |  **Name** |  **Description** |  
| R1101 |  CERTIFICATE_MISSING |  A required certificate is missing. |  
| R1102 |  CERTIFICATE_INVALID |  Certificate is invalid or unreadable. |  
| R1103 |  CERTIFICATE_EXPIRED |  Certificate has expired. |  
| R1104 |  CERTIFICATE_NOT_YET_VALID |  Certificate is not yet valid. |  
| R1105 |  CERTIFICATE_UNTRUSTED |  Certificate is not trusted. |  
| R1106 |  CERTIFICATE_AUTHORITY_INVALID |  Certificate authority is invalid. |  
| R1107 |  CERTIFICATE_CHAIN_INVALID |  Certificate chain is invalid. |  
| R1108 |  PRIVATE_KEY_MISSING |  Private key is missing. |  
| R1109 |  PRIVATE_KEY_INVALID |  Private key is invalid or unreadable. |  
| R1110 |  PRIVATE_KEY_PERMISSION_DENIED |  Insufficient permissions to access the private key. |  
| R1111 |  CERTIFICATE_KEY_MISMATCH |  Certificate and private key do not match. |  
| R1112 |  OPENSSL_NOT_FOUND |  OpenSSL executable was not found on the system. |  
| R1113 |  TLS_INITIALIZATION_FAILED |  Failed to initialize the TLS context. |  
  
   
**File system (R1200–R1299)**  
  
|  |  |  |  
| - | - | - |  
| **Code** |  **Name** |  **Description** |  
| R1201 |  FILE_NOT_FOUND |  Required file not found. |  
| R1202 |  FILE_READ_FAILED |  Failed to read a file. |  
| R1203 |  FILE_WRITE_FAILED |  Failed to write to a file. |  
| R1204 |  FILE_CORRUPTED |  File is corrupted or unusable. |  
| R1205 |  FILE_ALREADY_EXISTS |  A file with the same name already exists. |  
| R1206 |  DIRECTORY_NOT_FOUND |  Directory not found. |  
| R1207 |  DIRECTORY_CREATION_FAILED |  Failed to create a directory. |  
| R1208 |  DIRECTORY_ACCESS_DENIED |  Access to the directory was denied. |  
| R1209 |  DISK_SPACE_EXHAUSTED |  Insufficient disk space. |  
| R1210 |  PERMISSION_CHANGE_FAILED |  Failed to change permissions. |  
  
   
**Networking and connections (R1300–R1399)**  
  
|  |  |  |  
| - | - | - |  
| **Code** |  **Name** |  **Description** |  
| R1301 |  NETWORK_INITIALIZATION_FAILED |  Failed to initialize the network. |  
| R1302 |  PORT_ALREADY_IN_USE |  Requested port is already in use. |  
| R1303 |  PORT_ACCESS_DENIED |  Insufficient permissions to use the port. |  
| R1304 |  CONNECTION_REFUSED |  Connection was refused by the remote server. |  
| R1305 |  CONNECTION_TIMEOUT |  Connection timed out. |  
| R1306 |  CONNECTION_LOST |  Connection was lost. |  
| R1307 |  DNS_RESOLUTION_FAILED |  Failed to resolve the domain name. |  
| R1308 |  TLS_HANDSHAKE_FAILED |  TLS handshake failed. |  
| R1309 |  INVALID_REQUEST |  Network request is invalid. |  
| R1310 |  TOO_MANY_CONNECTIONS |  Maximum number of connections reached. |  
  
   
**Database (R1400–R1499)**  
  
|  |  |  |  
| - | - | - |  
| **Code** |  **Name** |  **Description** |  
| R1401 |  DATABASE_NOT_FOUND |  Database not found. |  
| R1402 |  DATABASE_CONNECTION_FAILED |  Failed to connect to the database. |  
| R1403 |  DATABASE_CORRUPTED |  Database is corrupted. |  
| R1404 |  DATABASE_ACCESS_DENIED |  Access to the database was denied. |  
| R1405 |  DATABASE_QUERY_FAILED |  Query execution failed. |  
| R1406 |  DATABASE_INITIALIZATION_FAILED |  Failed to initialize the database. |  
| R1407 |  DATABASE_LOCKED |  Database is locked. |  
| R1408 |  DATABASE_FULL |  Database is full. |  
| R1409 |  DATABASE_MIGRATION_FAILED |  Database migration failed. |  
  
   
**Logging and diagnostics (R1500–R1599)**  
  
|  |  |  |  
| - | - | - |  
| **Code** |  **Name** |  **Description** |  
| R1501 |  LOG_DIRECTORY_UNAVAILABLE |  Log directory is unavailable. |  
| R1502 |  LOG_FILE_CREATION_FAILED |  Failed to create a log file. |  
| R1503 |  LOG_WRITE_FAILED |  Failed to write to the logs. |  
| R1504 |  LOG_READ_FAILED |  Failed to read the logs. |  
| R1505 |  CRASH_LOG_CREATION_FAILED |  Failed to create a crash log. |  
| R1506 |  STACK_TRACE_WRITE_FAILED |  Failed to write the stack trace. |  
| R1507 |  STACK_TRACE_GENERATION_FAILED |  Failed to generate the stack trace. |  
| R1508 |  LOG_PERMISSION_DENIED |  Insufficient permissions to access the logs. |  
  
   
**System resources (R1600–R1699)**  
  
|  |  |  |  
| - | - | - |  
| **Code** |  **Name** |  **Description** |  
| R1601 |  MEMORY_ALLOCATION_FAILED |  Failed to allocate memory. |  
| R1602 |  MEMORY_LIMIT_REACHED |  Memory limit reached. |  
| R1603 |  CPU_OVERLOAD |  CPU load is unusually high. |  
| R1604 |  PROCESS_CREATION_FAILED |  Failed to create a process. |  
| R1605 |  PROCESS_EXECUTION_FAILED |  Process execution failed. |  
| R1606 |  DEPENDENCY_MISSING |  A required dependency is missing. |  
| R1607 |  DEPENDENCY_VERSION_MISMATCH |  Dependency version is incompatible. |  
| R1608 |  SYSTEM_RESOURCE_UNAVAILABLE |  A system resource is unavailable. |  
  
   
**Server lifecycle (R1700–R1799)**  
  
|  |  |  |  
| - | - | - |  
| **Code** |  **Name** |  **Description** |  
| R1701 |  SERVER_START_FAILED |  Failed to start the server. |  
| R1702 |  SERVER_STOP_FAILED |  Failed to stop the server cleanly. |  
| R1703 |  SERVER_UNEXPECTED_SHUTDOWN |  Server shut down unexpectedly. |  
| R1704 |  SERVER_CRASH |  The server crashed. |  
| R1705 |  SERVER_ALREADY_RUNNING |  A server instance is already running. |  
| R1706 |  SERVER_NOT_RUNNING |  The server is not running. |  
| R1707 |  SERVER_UNRESPONSIVE |  The server is not responding. |  
| R1708 |  SERVER_CONFIGURATION_ERROR |  Server configuration is invalid. |  
  
   
**Warnings (W1000–W1999)**  
  
|  |  |  |  
| - | - | - |  
| **Code** |  **Name** |  **Description** |  
| W1001 |  FOLDER_ALREADY_EXISTS |  A folder already exists. |  
| W1002 |  CERTIFICATE_EXPIRING_SOON |  A certificate will expire soon. |  
| W1003 |  LOW_DISK_SPACE |  Disk space is running low. |  
| W1004 |  HIGH_MEMORY_USAGE |  Memory usage is high. |  
| W1005 |  HIGH_CPU_USAGE |  CPU usage is high. |  
| W1006 |  OPENSSL_UNAVAILABLE |  OpenSSL is unavailable for an operation that requires it. |  
| W1007 |  AUDIO_NOTIFICATION_FAILED |  Failed to play the audio notification. |  
| W1008 |  LOG_ROTATION_REQUIRED |  Log rotation is recommended. |  
| W1009 |  CONFIGURATION_DEFAULT_USED |  A default configuration was used. |  
| W1010 |  NON_CRITICAL_DEPENDENCY_MISSING |  A non-critical dependency is missing. |  
| W1011 |  NO\_SERVER_KNOWN |  known_servers.json is empty, the program did not know any others servers. |  
| W1012 |  NO\_USERS_KNOWN |  known_users.json is empty, the program did not know any others users. |  
  
   
**Information (I1000–I1999)**  
  
|  |  |  |  
| - | - | - |  
| **Code** |  **Name** |  **Description** |  
| I1001 |  INITIALIZATION_STARTED |  Initialization started. |  
| I1002 |  INITIALIZATION_COMPLETED |  Initialization completed. |  
| I1003 |  FOLDER_CREATED |  Folder created. |  
| I1004 |  CERTIFICATES_VERIFIED |  Certificates verified. |  
| I1005 |  DATABASE_CONNECTED |  Database connection established. |  
| I1006 |  SERVER_STARTED |  Server started. |  
| I1007 |  SERVER_STOPPED |  Server stopped. |  
| I1008 |  CONNECTION_ESTABLISHED |  New connection established. |  
| I1009 |  CONNECTION_CLOSED |  Connection closed. |  
| I1010 |  CRASH_LOG_CREATED |  Crash log created. |  
  
   
