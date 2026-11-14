# Initialization
from pathlib import Path
from datetime import datetime
import subprocess
import time

# Variable
parent_dir = Path(__file__).resolve().parent.parent
folder = ["Config", "Public", "assets", "logs", "database", "Stock"]
today_date = datetime.today().strftime("%Y-%m-%d")
current_time = datetime.now().strftime("%H:%M:%S")
logs_file_name_and_location = parent_dir / "logs" / f"logs_{today_date}.txt"
# Definition
def bip_erreur():
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
    print(f"[{current_time}]Error during initialisation : {e}")
    bip_erreur()
    try:
        # Logging
        with open(logs_file_name_and_location, "a", encoding="utf-8") as f:
                f.write(f"[{current_time}] Error : {e}\n")
    except: # log error, pass
        exit()


else:
    print(f"[{current_time}]Successfully Initialized Raitile Shop (Server Side)")
