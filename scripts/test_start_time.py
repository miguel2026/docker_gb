import time
import subprocess
from pathlib import Path
def measure_start_time(cmd_up, cmd_down, cwd):
    cwd = Path(__file__).resolve().parent.parent / "docker"
    cwd = str(cwd)
    subprocess.run(cmd_down, cwd=cwd, stdout=subprocess.DEVNULL)
    start = time.time()
    subprocess.run(cmd_up, cwd=cwd, stdout=subprocess.DEVNULL)
    duration = time.time() - start
    return round(duration, 2)

def measure_start_time_windows(cmd_up, cmd_down):
    subprocess.run(cmd_down, stdout=subprocess.DEVNULL)
    start = time.time()
    subprocess.run(cmd_up, stdout=subprocess.DEVNULL)
    duration = time.time() - start
    return round(duration, 2)