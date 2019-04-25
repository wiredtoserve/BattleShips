import subprocess
import time

counter = 100

while counter:
    subprocess.run(["python3", "main.py"])
    time.sleep(0.5)
    counter -= 1

# stats = {}
# with open('logfile.txt', 'r') as f:
#     data = f.readlines()
#     stats['Goose'] = 0
#     stats['Iceman'] = 0
#     for i in data:
#         if i.split():
#             # Player 1
#             if i.split()[1] == '1':
#                 stats['Goose'] += 1
#             # Player 0
#             elif i.split()[1] == '0':
#                 stats['Iceman'] += 1
#
# print(f'Statistics - {stats}')