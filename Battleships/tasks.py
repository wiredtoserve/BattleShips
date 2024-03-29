# Task file that contains the classes
# Should pass the complete class as String to main.py

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

    def setup_ships(self):
        '''

        :return: a 10x10 grid with the location of our ships
        '''
        grid = [[0 for i in range(10)] for j in range(10)]

        # ship numbers
        ship = [i for i in range(1, 6)]

        # randomly shuffle the ship list
        Player.random.shuffle(ship)

        for ship_number in ship:
            control = True

            while control:
                # randomly select a point on the grid
                ship_start_position = self.random_position()

                if self.vacant(ship_start_position, ship_number, grid):
                    for row in range(0, ship_number):
                        # print(f'{ship_start_position} ship : {ship_number}')
                        grid[ship_start_position[0] + row][ship_start_position[1]] = ship_number

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
        last_shot = history[-1]['incoming']
        self.player_battleground = self.update_opponent_shots(self.player_battleground, last_shot)

        # counting the number of ships left
        self.ships_dd = Player.defaultdict(int)  # reset count everytime
        # ships_dd = Player.defaultdict(int)

        for row in self.player_battleground:
            for point in row:
                self.ships_dd[point] += point

        self.status = self.ship_status(self.ships_dd)

        # Count the number of ships remaining
        number_of_ships = len(self.status)

        # Take random shots
        shots_list = [number for number in self.random_shots(number_of_ships)]

        # return [(0, 0), (1, 1), (2, 2)]
        # return Player.setup_ships(self)
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
    def vacant(self, pos, ship, grid):
        # checking if the ship will fit in the board
        if pos[0] + ship <= 10:
            for i in range(0, ship):
                # checking if any other ship is already present
                if grid[pos[0] + i][pos[1]] != 0:
                    return False
            return True
        return False

    def random_shots(self, num=5):
        for x in range(0, num):
            yield Player.random.randint(0, 9), Player.random.randint(0, 9)

    def update_opponent_shots(self, grid, incoming_shots):
        for x, y in incoming_shots:
            grid[x][y] = 9
        return grid

    def ship_status(self, ships_dd):
        status = []
        for ship in ships_dd.keys():
            # as long as the default dictionary has a key, the ship is breathing
            if ship in [1, 2, 3, 4, 5]:
                status.append((ship, ships_dd[ship] / (ship ** 2)))

        return status