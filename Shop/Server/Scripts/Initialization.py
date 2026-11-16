# Initialization
from pathlib import Path
from datetime import datetime
import subprocess
import shutil
import time
import sys
import os

# Variable
parent_dir = Path(__file__).resolve().parent.parent
public_folders = ["Public", "assets"]
private_folders = ["Config", "logs", "database", "Stock", "certs"]
required_certs = ["ca.crt", "server.crt", "server.key"]
today_date = datetime.today().strftime("%Y-%m-%d")
logs_file_name_and_location = parent_dir / "logs" / f"logs_{today_date}.txt"
stack_trace = ["----------------------------------Begin Stack Trace--------------------------------\n"]

# Colors
RESET = "\033[0m"
ORANGE = "\033[38;5;208m"
YELLOW = "\033[93m"
RED = "\033[91m"
GREEN = "\033[92m"

# Definition
def bip_error():
    if shutil.which("aplay") is None:
        return
    bip = (b'\x00' * 10 + b'\xff' * 10) * 80
    fin = time.time() + 5

    while time.time() < fin:
        debut_cycle = time.time()
        subprocess.run(['aplay', '-q'], input=bip, stderr=subprocess.DEVNULL)
        
        pause = 0.8 - (time.time() - debut_cycle)
        if pause > 0:
            time.sleep(pause)

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def next_crash_log_path():
    crash_log_id = 1
    while True:
        candidate = parent_dir / "logs" / f"crash_logs_{today_date}_{crash_log_id}.txt"
        if not candidate.exists():
            return candidate
        crash_log_id += 1

Stack_trace_location = next_crash_log_path()

def writing_stack_trace(crash):
    if crash == True:
        with open(Stack_trace_location, "a", encoding="utf-8") as f:
            f.write("".join(stack_trace))
        with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
            f.write("".join(stack_trace))
    else:
        with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
            f.write("".join(stack_trace))

if __name__ == "__main__":
    try:
        # Creating folders & permissions
        for folder in public_folders:
            (parent_dir / folder).mkdir(exist_ok=True, parents=True)
            stack_trace.append(f"[{now()}] Created public folder: {folder}\n")

        for folder in private_folders:
            folder_path = parent_dir / folder
            folder_path.mkdir(exist_ok=True, parents=True)
            stack_trace.append(f"[{now()}] Created private folder: {folder}\n")
            if os.name != "nt":
                os.chmod(folder_path, 0o700)

        # Checking certificates
        certs_dir = parent_dir / "certs"
        for cert in required_certs:
            if not (certs_dir / cert).is_file():
                stack_trace.append(f"[{now()}] Missing security certificate: {cert} in {certs_dir}\n")
                raise FileNotFoundError(f"Missing security certificate: {cert} in {certs_dir}")
        stack_trace.append(f"[{now()}] All required security certificates are present.\n")

        if os.name != "nt":
            os.chmod(certs_dir / "server.key", 0o600)
            stack_trace.append(f"[{now()}] Set permissions for server.key to 600\n")

        # Logging
        with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
            f.write(f"[{now()}] Initialization completed.\n")
            stack_trace.append(f"[{now()}] Initialization completed.\n")

    except Exception as e:
        print(f"{RED}[{now()}] Error during initialisation : {e}{RESET}")
        stack_trace.append(f"[{now()}] Error during initialisation : {e}\n")
        try:
            bip_error()
            stack_trace.append(f"[{now()}] Audio notification sent.\n")
        except Exception as audio_error:
            print(f"{ORANGE}[{now()}] WARNING : Audio notification failed{RESET}")
            stack_trace.append(f"[{now()}] WARNING : Audio notification failed : {audio_error}\n")
            try:
                with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
                    stack_trace.append(f"[{now()}] WARNING : {audio_error}\n")
                    f.write(f"[{now()}] WARNING : {audio_error}\n")
            except Exception as log_error:
                print(f"{ORANGE}[{now()}] WARNING : log failed : {log_error}{RESET}")
                print(f"{YELLOW}[{now()}] Stack trace cannot be written !{RESET}")
                print(f"{YELLOW}[{now()}] Please check the permissions of the logs folder and try again.{RESET}")
                print(f"{YELLOW}[{now()}] If the problem persists, please contact support.{RESET}")
                print(f"{YELLOW}[{now()}] Giving stack trace :{RESET}")
                print(f"{YELLOW}{''.join(stack_trace)}{RESET}")

        try:
            with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
                f.write(f"[{now()}] Error : {e}\n")
                stack_trace.append(f"[{now()}] Error : {e}\n")
        except Exception as log_error:
            print(f"{ORANGE}[{now()}] WARNING : log failed : {log_error}{RESET}")
            print(f"{YELLOW}[{now()}] Stack trace cannot be written !{RESET}")
            print(f"{YELLOW}[{now()}] Please check the permissions of the logs folder and try again.{RESET}")
            print(f"{YELLOW}[{now()}] If the problem persists, please contact support.{RESET}")
            print(f"{YELLOW}[{now()}] Giving stack trace :{RESET}")
            print(f"{YELLOW}{''.join(stack_trace)}{RESET}")
        stack_trace.append(f"[{now()}] Exiting with error code 1\n")
        stack_trace.append(f"[{now()}] Stack trace written to {Stack_trace_location}\n")
        stack_trace.append("----------------------------------Ending Stack Trace-------------------------------\n")
        writing_stack_trace(crash=True)
        print(f"{RED}[{now()}] Exiting with error code 1{RESET}")
        print(f"{YELLOW}[{now()}] Stack trace(the most important part) :{RESET}")
        print(f"{YELLOW}{''.join(stack_trace)}{RESET}")
        sys.exit(1)

    else:
        print(f"{GREEN}[{now()}] Successfully Initialized Raitile Shop (Server Side){RESET}")
        stack_trace.append(f"[{now()}] Initialization completed successfully.\n")
        stack_trace.append(f"[{now()}] ------------------------------ Initialization Trace completed ------------------------------\n")
        writing_stack_trace(crash=False)
