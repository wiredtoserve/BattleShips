class Player:
    """
    Contains three methods
        1. setup_ships: takes no parameters and returns a list of lists showing the start position
                        of showing the start positions of your ships
                        Block of row i and column j, ship label 1-5 & 0 means no ship

        2. take_turn:   returns
                        -- a list of (row, column) tuples describing your shots
                        -- eg: [(1, 1), (1, 3), (1, 5), (2, 1) (4, 5)]
                        -- Note: should be equal to the number of ships present (check function)
                        -- or a tuple that has a ship number as the first element and the direction
                        -- of its moving value
                        -- 0: up, 1: right, 2: down, 3: left  (dict)

                        TODO: Do not take more shots than the number of ships
                        TODO: Do not move the ships outside the grid or radioactive zone

        3. get_name:   returns a string that is the name of the Player

    """
    import random
    from collections import defaultdict

    def __init__(self):

        self.player_battleground = [[0 for i in range(10)] for j in range(10)]
        self.opponent_battleground = [[0 for i in range(10)] for j in range(10)]

        self.ships_dd = Player.defaultdict(int)
        self.status = []

        self.enemy_dict = {(i, j): 0 for i in range(10) for j in range(10)}

        # number of turns
        self.counter = 0

        # total number of hits
        self.hits = 0

    def setup_ships(self):
        '''

        :return: a 10x10 grid with the location of our ships
        '''
        grid = [[0 for i in range(10)] for j in range(10)]

        # ship numbers
        ship = [i for i in range(1, 6)]

        # randomly shuffle the ship list
        Player.random.shuffle(ship)

        # select direction
        # 1 - down, 2 - right
        direction = [1, 2]

        for ship_number in ship:
            control = True

            while control:
                # randomly select a point on the grid
                ship_start_position = self.random_position()

                # randomly select the direction to be placed
                orientation = Player.random.choice(direction)

                if self.vacant(ship_start_position, ship_number, grid, orientation):
                    for row in range(0, ship_number):
                        # print(f'{ship_start_position} ship : {ship_number}')
                        if orientation == 1:
                            grid[ship_start_position[0] + row][ship_start_position[1]] = ship_number
                        elif orientation == 2:
                            grid[ship_start_position[0]][ship_start_position[1] + row] = ship_number

                    control = False

        self.player_battleground = grid
        return grid

    def take_turn(self, history):
        '''

        :param history: records the game
                        list that contains one entry per turn
                        dict with 3 keys
                            - 'shots' : list of shots made in the turn
                            - 'hits' : an integer number of hits that your shots made
                            - 'incoming' : opponents list of shots, [] if moved

        :return: a list of tuple/s describing the shots or changed location
                depending on the strategy
        '''
        # last_shot = history[-1]['incoming']
        # TODO: use history to short circuit the take_turn function
        # TODO: consider if the opponent moves

        last_shot = history[-1]['incoming'] if self.counter > 0 else []

        self.player_battleground = self.update_opponent_shots(self.player_battleground, last_shot)

        # counting the number of ships left
        self.ships_dd = Player.defaultdict(int)  # reset count every time
        # ships_dd = Player.defaultdict(int)

        # returns the dict with the number of ships and hits
        for row in self.player_battleground:
            for point in row:
                self.ships_dd[point] += point

        self.status = self.ship_status(self.ships_dd)

        # Count the number of ships remaining
        number_of_ships = len(self.status) if self.status else []

        player_shots = history[-1]['shots'] if self.counter > 0 else []
        if self.counter > 0:
            self.hits += history[-1]['hits']

        # updating the shots taken by the player
        # self.enemy_dict = self.update_enemy_dict(self.enemy_dict, player_shots)
        self.update_enemy_dict(player_shots)

        if self.counter > 0 and history[-1]['hits']:
            # If the Player hit in its last turn, update the minesweeper matrix
            # then choose to shoot at the highest probable locations
            turn_hits = history[-1]['hits']
            self.enemy_dict = self.minesweeper(self.enemy_dict, player_shots, turn_hits)
            shots_list = [number for number in self.shot_generator(self.enemy_dict, number_of_ships)]

        # elif self.counter > 0 or history[-1]['hits'] == 0:
        #     shots_list = [number for number in self.random_selection(self.enemy_dict, number_of_ships)]

        else:
            # In case of the first shot, hits = 0 and it will shoot randomly
            # However, if the Player has already had some hits, the player will
            # use the minesweeper matrx and try again randomly at the more probable locations
            shots_list = [number for number in self.random_selection(self.enemy_dict, self.hits, number_of_ships)]

        # update the number of turns
        self.counter += 1

        return shots_list

    def get_name(self):
        '''

        :return: string - name of the Player
        '''
        return "Syndicate_10"

    # function to select a point on the grid
    def random_position(self):
        return [Player.random.randint(0, 9), Player.random.randint(0, 9)]

    # function to check if the position is vacant
    def vacant(self, pos, ship, grid, orientation):
        # checking the direction to place the ship
        if orientation == 1:
            # checking if the ship will fit in the board
            if pos[0] + ship <= 10:
                for i in range(0, ship):
                    # checking if any other ship is already present
                    if grid[pos[0] + i][pos[1]] != 0:
                        return False
                return True
        elif orientation == 2:
            # checking if the ship will fit in the board
            if pos[1] + ship <= 10:
                for i in range(0, ship):
                    # checking if any other ship is already present
                    if grid[pos[0]][pos[1] + i] != 0:
                        return False
                return True
        return False

        # function to shoot randomly with a given number of ships

    def random_shots(self, num=5):
        for x in range(0, num):
            yield Player.random.randint(0, 9), Player.random.randint(0, 9)

    # function to update the player battleground with the incoming shots
    def update_opponent_shots(self, grid, incoming_shots):
        if incoming_shots:
            for x, y in incoming_shots:
                grid[x][y] = 9
        return grid

    # function that counts the number of ships and her ports hit
    def ship_status(self, ships_dd):
        status = []
        for ship in ships_dd.keys():
            # as long as the default dictionary has a key, the ship is breathing
            if ship in [1, 2, 3, 4, 5]:
                status.append((ship, ships_dd[ship] / (ship ** 2)))
        return status

    # function to update the opponent battleground with the shots taken
    def update_enemy_dict(self, player_shots):
        if player_shots:
            for i, j in player_shots:
                self.enemy_dict[(i, j)] = -1

    # minesweeper matrix update
    def minesweeper(self, enemy_dict, player_shots, turn_hits):

        # up, down, right, left, upright, downright, up-left, down-left
        # minesweeper = [(-1, 0), (1, 0), (0, 1), (0, -1), (-1, 1), (1, 1), (-1, -1), (1, -1)]
        # up, down, right, left
        minesweeper = [(-1, 0), (1, 0), (0, 1), (0, -1)]

        # updating the enemy dictionary
        # only if it has hit!
        for i, j in player_shots:
            # opponent_battleground[i][j] = -1
            for x, y in minesweeper:
                # checking if the next position is in the board
                if (x + i) >= 0 and (x + i) <= 9 and (y + j) >= 0 and (y + j) <= 9:
                    # checking if it has already not been hit
                    if enemy_dict[(i + x, j + y)] != -1:
                        enemy_dict[(i + x, j + y)] += turn_hits # TODO: check effectiveness

        return enemy_dict

    # shot generator based on the minesweeper
    def shot_generator(self, enemy_dict, num=5):
        sorted_shot_list = sorted([(i[1], i[0]) for i in enemy_dict.items()], reverse=True)
        for i in range(num):
            yield sorted_shot_list[i][1]

    # function that randomly selects positions to hit and removes them
    def random_selection(self, enemy_dict, hits, num=5):
        sorted_shot_list = sorted([(i[1], i[0]) for i in enemy_dict.items() if i[1] >= 0], reverse=True)

        # If the number of ships are greater than your shots space
        if num > len(sorted_shot_list):
            num = len(sorted_shot_list)

        # If there are existing hits, choose to select randomly from the higher weighted points
        if not hits:
            shot = Player.random.sample(sorted_shot_list, k=num)
        else:
            shot = Player.random.sample(sorted_shot_list[:7], k=num)

        shot_list = [i[1] for i in shot]

        return shot_list
