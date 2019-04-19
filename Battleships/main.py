"""
    Simple battleships game for MBUSA90500 Programming.
    main file to send to the server

    Syndicate 10
    Thu 17 Apr 2019 21:30:00 AEST

    Command to be sent to the server as JSON objects
        - 'cmd': ADD, DEL, TEST (Add players, Delete Players, Test)
        - 'syn': 10 (Syndicate Number)
        - 'name': team name
        - 'data': value of string, python code

        - 'data2': only enabled in TEST mode, for the second player

"""

import json
import socket

# Global Variables defined
SYNDICATE_NUMBER = 10
COMMAND = 'DEL' # 'ADD', 'DEL', 'TEST'
SYNDICATE_NAME = 'pyflake'


def send_to_server(js):
    """Open socket and send the json string js to server with EOM appended, and wait
       for \n terminated reply.
       js - json object to send to server
    """
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect(('128.250.106.25', 5002))
    clientsocket.send("""{}EOM""".format(js).encode('utf-8'))
    data = ''
    while data == '' or data[-1] != "\n":
        data += clientsocket.recv(1024).decode('utf-8')
    print(data)

    clientsocket.close()

# NOTE: call the player string from tasks.py

#p = "class Player:..."
#p2 = "class Player:..."

# reading the test.py file in as string
with open('tasks.py', 'r') as f:
    p = f.read()
    #p2 = p

with open('test.py', 'r') as f:
    p2 = f.read()

# player dictionary
if COMMAND == 'TEST':
    p_dict = {"cmd":COMMAND, "syn":SYNDICATE_NUMBER, "name":SYNDICATE_NAME, "data":p, "data2":p2}
else:
    p_dict = {"cmd":COMMAND, "syn":SYNDICATE_NUMBER, "name":SYNDICATE_NAME, "data":p}

#rint(p_dict)


#send_to_server(json.dumps({"cmd":"TEST", "syn":10, "name":"T4", "data":p, "data2":p2}))
#send_to_server(json.dumps({"cmd":"ADD", "syn":10, "name":"starflake", "data":p}))

send_to_server(json.dumps(p_dict))

#print(p)
