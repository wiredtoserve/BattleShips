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


# p = "class Player:..."
# p2 = "class Player:..."

# send_to_server(json.dumps({"cmd":"TEST", "syn":10, "name":"T4", "data":p, "data2":p2}))

print('Hello World')
