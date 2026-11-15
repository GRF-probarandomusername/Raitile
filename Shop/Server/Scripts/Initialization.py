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

if __name__ == "__main__":
    try:
        # Creating folders & permissions
        for folder in public_folders:
            (parent_dir / folder).mkdir(exist_ok=True, parents=True)

        for folder in private_folders:
            folder_path = parent_dir / folder
            folder_path.mkdir(exist_ok=True, parents=True)
            if os.name != "nt":
                os.chmod(folder_path, 0o700)

        # Checking certificates
        certs_dir = parent_dir / "certs"
        for cert in required_certs:
            if not (certs_dir / cert).is_file():
                raise FileNotFoundError(f"Missing security certificate: {cert} in {certs_dir}")

        if os.name != "nt":
            os.chmod(certs_dir / "server.key", 0o600)

        # Logging
        with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
            f.write(f"[{now()}] Initialization completed.\n")

    except Exception as e:
        print(f"{RED}[{now()}] Error during initialisation : {e}{RESET}")
        try:
            bip_error()
        except Exception as audio_error:
            print(f"{ORANGE}[{now()}] WARNING : Audio notification failed{RESET}")
            try:
                with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
                    f.write(f"[{now()}] WARNING : {audio_error}\n")
            except Exception as log_error:
                print(f"{ORANGE}[{now()}] WARNING : log failed : {log_error}{RESET}")

        try:
            with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
                f.write(f"[{now()}] Error : {e}\n")
        except Exception as log_error:
            print(f"{ORANGE}[{now()}] WARNING : log failed : {log_error}{RESET}")
        
        sys.exit(1)

    else:
        print(f"{GREEN}[{now()}] Successfully Initialized Raitile Shop (Server Side){RESET}")
