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
COMMAND = 'TEST'  # 'ADD', 'DEL', 'TEST'
SYNDICATE_NAME = 'Viper'  # 'Maverick', 'Goose', Iceman, 'starflake', 'Viper', 'Merlin', 'Charlie'


# def send_to_server(js):
#     """Open socket and send the json string js to server with EOM appended, and wait
#        for \n terminated reply.
#        js - json object to send to server
#     """
#     clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     clientsocket.connect(('128.250.106.25', 5002))
#     clientsocket.send("""{}EOM""".format(js).encode('utf-8'))
#     data = ''
#     while data == '' or data[-1] != "\n":
#         data += clientsocket.recv(1024).decode('utf-8')
#     print(data)
#
#     # Added to log the results
#     with open('logfile', 'w') as f:
#         f.write(data)
#
#     clientsocket.close()

def send_to_server(js):
    """Open socket and send the json string js to server with EOM appended, and wait
       for \n terminated reply.
       js - json object to send to server
    """
    try:
        clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientsocket.connect(('128.250.106.25', 5002))
        clientsocket.send("""{}EOM""".format(js).encode('utf-8'))
        data = ''
        while data == '' or data[-1] != "\n":
            data += clientsocket.recv(1024).decode('utf-8')
        print(data)

        # Added to log the results
        with open('logfile.txt', 'a+') as logger:
            logger.write(data + '\n')

        clientsocket.close()

    except Exception as e:
        print("Error: ", e)
        # Added to log the results
        # with open('logfile.csv', 'w') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(str(e))
        with open('logfile.txt', 'a+') as f:
            f.write(str(e) + '\n')


# reading the test.py file in as string
with open('tasks.py', 'r') as f:
    p_dummy = f.read()
    # p2 = p

# random shooting
with open('test.py', 'r') as f:
    p_iceman1 = f.read()

# probability included in shooting
with open('test_charlie.py', 'r') as f:
    p_charlie = f.read()

# minesweeper functionality in shooting
with open('test_goose.py', 'r') as f:
    p_goose = f.read()

with open('test_iceman.py', 'r') as f:
    p_iceman = f.read()

with open('test_merlin.py', 'r') as f:
    p_merlin = f.read()

with open('test_viper.py', 'r') as f:
    p_viper = f.read()

# player dictionary
if COMMAND == 'TEST':
    p_dict = {"cmd": COMMAND, "syn": SYNDICATE_NUMBER, "name": SYNDICATE_NAME, "data": p_charlie, "data2": p_viper}
else:
    if SYNDICATE_NAME == 'Iceman':
        p_dict = {"cmd": COMMAND, "syn": SYNDICATE_NUMBER, "name": SYNDICATE_NAME, "data": p_iceman}
    elif SYNDICATE_NAME == 'Goose':
        p_dict = {"cmd": COMMAND, "syn": SYNDICATE_NUMBER, "name": SYNDICATE_NAME, "data": p_goose}
    elif SYNDICATE_NAME == 'Charlie':
        p_dict = {"cmd": COMMAND, "syn": SYNDICATE_NUMBER, "name": SYNDICATE_NAME, "data": p_charlie}
    elif SYNDICATE_NAME == 'Merlin':
        p_dict = {"cmd": COMMAND, "syn": SYNDICATE_NUMBER, "name": SYNDICATE_NAME, "data": p_merlin}
    elif SYNDICATE_NAME == 'Viper':
        p_dict = {"cmd": COMMAND, "syn": SYNDICATE_NUMBER, "name": SYNDICATE_NAME, "data": p_viper}
    elif SYNDICATE_NAME == 'starflake':
        p_dict = {"cmd": COMMAND, "syn": SYNDICATE_NUMBER, "name": SYNDICATE_NAME, "data": p_dummy}

    else:
        p_dict = None
        print('Error while submitting, please check your input')

# print(p_dict)

if p_dict:
    send_to_server(json.dumps(p_dict))
