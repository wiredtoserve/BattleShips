# Task file that contains the classes
# Should pass the complete class as String to main.py

#import random

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

    def setup_ships(self):
        '''

        :return: a 10x10 grid with the location of our ships
        '''
        # Grid of rows and columns ranging from indices 0 to 9
        grid = [[0 for i in range(10)] for j in range(10)]
        for ship in range(1, 6):
            for row in range(0, ship):
                grid[row][ship] = ship
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
        return [(0, 0), (1, 1), (2, 2)]

    def get_name(self):
        '''

        :return: string - name of the Player
        '''
        return "Syndicate_10"


# This part of the code is just for demonstration only

class DummyPlayer:
    """

    Dummy player for test purposes

    """
    import random

    def setup_ships(self):
        '''

        :return: a 10x10 grid with the location of our ships
        '''
        grid = [[0 for i in range(10)] for j in range(10)]

        # ship numbers
        ship = [i for i in range(1, 6)]

        # randomly shuffle the ship list
        DummyPlayer.random.shuffle(ship)

        for ship_number in ship:
            control = True

            while control:
                # randomly select a point on the grid
                ship_start_position = self.random_position()

                if self.vacant(ship_start_position, ship_number, grid):
                    for row in range(0, ship_number):
                        grid[ship_start_position[0] + row][ship_start_position[1]] = ship_number

                    control = False

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
        return [(0, 0), (1, 1), (2, 2)]

    def get_name(self):
        '''

        :return: string - name of the Player
        '''
        return "Syndicate_10"

    # function to select a point on the grid
    def random_position(self):
        return [DummyPlayer.random.randint(0, 9), DummyPlayer.random.randint(0, 9)]

    # function to check if the position is vacant
    def vacant(self, pos, ship, grid):
        # checking if the ship will fit in the board
        if pos[0] + ship <= 10:
            for i in range(0, ship):
                # checking if any other ship is already present
                if grid[i][pos[1]] != 0:
                    return False
            return True
        return False


p1 = DummyPlayer()
print(p1.get_name())
grid = p1.setup_ships()
for i in grid:
    print(i)
