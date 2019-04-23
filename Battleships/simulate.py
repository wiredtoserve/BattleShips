import subprocess
import time

counter = 10

while counter:
    subprocess.run(["python3", "main.py"])
    time.sleep(0.5)
    counter -= 1