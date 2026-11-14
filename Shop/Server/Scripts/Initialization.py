# Initialization
from pathlib import Path
from datetime import datetime
import subprocess
import time
import sys

# Variable
parent_dir = Path(__file__).resolve().parent.parent
folder = ["Config", "Public", "assets", "logs", "database", "Stock"]
today_date = datetime.today().strftime("%Y-%m-%d")
current_time = datetime.now().strftime("%H:%M:%S")
logs_file_name_and_location = parent_dir / "logs" / f"logs_{today_date}.txt"
# Colors
RESET = "\033[0m"
ORANGE = "\033[38;5;208m"
YELLOW = "\033[93m"
RED = "\033[91m"
GREEN = "\033[92m"
# Definition
def bip_error():
    bip = (b'\x00' * 10 + b'\xff' * 10) * 80
    fin = time.time() + 5

    while time.time() < fin:
        debut_cycle = time.time()
        subprocess.run(['aplay', '-q'], input=bip, stderr=subprocess.DEVNULL)
        
        pause = 0.8 - (time.time() - debut_cycle)
        if pause > 0:
            time.sleep(pause)

# asynchronized definition

# try

try:
    # Creating folders
    for folders in folder:
        (parent_dir / folders).mkdir(exist_ok=True, parents=True)
    # Logging
    with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
        f.write(f"[{current_time}] Initialization completed.\n")
except Exception as e:
    print(f"{RED}[{current_time}]Error during initialisation : {e}{RESET}")
    try:
        bip_error()
    except Exception as audio_error:
        print(f"{ORANGE}WARNING : Audio notification failed{RESET}")
        try:
            # Logging
            with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
                    f.write(f"[{current_time}] WARNING : {audio_error}\n")
        except Exception as log_error: # log has failed, nothing
            print(f"{ORANGE}WARNING : log failed : {log_error}{RESET}")
    try:
        # Logging
        with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
                f.write(f"[{current_time}] Error : {e}\n")
    except Exception as log_error: # log has failed, nothing
        print(f"{ORANGE}WARNING : log failed : {log_error}{RESET}")
        sys.exit(1)
else:
    print(f"{GREEN}[{current_time}]Successfully Initialized Raitile Shop (Server Side){RESET}")
