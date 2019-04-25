# Helper File to house all the additional functions
'''

Defense
Random Placement of ships:
Iceman, Goose, Charlie

Optimal Placement of ships:
Merlin, Viper*

Attack:
Probability - Charlie, Merlin
Probability 2.0 - Viper*
Minesweeper - Iceman
Weighted_Minesweeper - Goose

TODO: If Merlin looses less, update Goose to Optimal Placement

'''

import random


class Ball:
    def __init__(self, name, radius):
        self.name = 'Mehul'
        assert (type(name) == str)
        assert (type(radius) == int)

    def __repr__(self): return self.name


b = Ball('Mike', 30)


# print(b) # prints the __repr__ return

# count ships
# random shot
# probability of hits
# updating the hit matrix


# variables: myport, enenmy port
# def shot, move, update_myport, update_enemyport

def random_shots(num=5):
    for x in range(0, num):
        yield random.randint(0, 9), random.randint(0, 9)


# Generating the history randomly
mydict = {'shots': [], 'hits': 0, 'incoming': []}
history_list = []


def generate_history(history_list=[], reset=False):
    if reset:
        return []
    else:

        shots_list = [number for number in random_shots()]
        hits = random.randint(0, 5)
        incoming_list = [number for number in random_shots()]

        mydict['shots'] = shots_list
        mydict['hits'] = hits
        mydict['incoming'] = incoming_list

        return mydict


def hist_generator(num=5):
    for x in range(0, num):
        yield generate_history()

history = []
for obj in hist_generator():
    temp = obj.copy()
    history += [temp]

#print(history)

opponent_grid = [[0 for i in range(10)] for j in range(10)]
last_shot = history[-1]['incoming']

def update_opponent(opponent_grid, incoming_shots):
    for x, y in incoming_shots:
        opponent_grid[x][y] = '*'
    return opponent_grid

update_opponent(opponent_grid, last_shot)

for i in update_opponent(opponent_grid, last_shot):
    print(i)
