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

        3. get_name:   returns a string that is the name of the Player

    """
    import random
    from collections import defaultdict

    def __init__(self):

        self.player_battleground = [[0 for i in range(10)] for j in range(10)]

        self.ships_dd = Player.defaultdict(int)
        self.status = []

        self.enemyport = [[0 for i in range(10)] for j in range(10)]

        # Set up the probability map.
        self.enemy_probmap = [[15 for i in range(10)] for j in range(10)]

        # TODO: Remove this
        self.potential_list = [(i, j) for i in range(10) for j in range(10)]

        # number of turns
        self.counter = 0

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
        # last_shot = history[-1]['incoming']
        # TODO: use history to short circuit the take_turn function

        last_shot = []
        if self.counter > 0:
            last_shot = history[-1]['incoming']

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
        number_of_ships = len(self.status)

        # Updating the opponents probability matrix
        self.update_enemy_probmap(history)

        # updating the enemy port
        previous_shots = []
        if self.counter > 0:
            previous_shots = history[-1]['shots']

        self.enemyport = self.update_enemy_map(self.enemyport, previous_shots)

        # Based on some logic here, choose to shoot
        # using probability

        shots_list = self.shot(number_of_ships)

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
    def vacant(self, pos, ship, grid):
        # checking if the ship will fit in the board
        if pos[0] + ship <= 10:
            for i in range(0, ship):
                # checking if any other ship is already present
                if grid[pos[0] + i][pos[1]] != 0:
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

    # function that randomly selects positions to hit and removes them
    def random_selection(self, potential_list, num=5):

        if num > len(self.potential_list):
            # If the number of shots remaining are less than the actual ships
            num = len(self.potential_list)

        for x in range(0, num):
            shot = Player.random.choice(self.potential_list)
            self.potential_list.remove(shot)

            yield shot

    def update_enemy_probmap(self, history):
        # reset enemy_probmap
        self.enemy_probmap = [[-1 for i in range(10)] for j in range(10)]

        total_hit = 0
        total_shot = 0
        for turn in history:
            # record the success rate of each shot in enemy_probmap
            if turn['shots']:
                prob = int(turn['hits'] / len(turn['shots']) * 100 + 0.5)
                for i in turn['shots']:
                    self.enemy_probmap[i[0]][i[1]] = prob
            total_hit += turn['hits']
            total_shot += len(turn['shots'])

        # update the probablity of spots that have not been shots.
        prob = int((15 - total_hit) / (100 - total_shot) * 100 + 0.5)
        for row in range(10):
            for column in range(10):
                if self.enemy_probmap[row][column] == -1:
                    self.enemy_probmap[row][column] = prob

    def update_enemy_map(self, enemyport, previous_shots):
        if previous_shots:
            for x, y in previous_shots:
                enemyport[x][y] = 9
        return enemyport

        # Function that generate the list of shots
    def shot(self, myship_number):
        """
        Store the "coordinates of spots that have not been shot"
        into the list called "targets" and shuffle them to add randomness
        """
        targets = []
        for row in range(10):
            for column in range(10):
                if self.enemyport[row][column] == 0:
                    targets.append((row, column))
        Player.random.shuffle(targets)
        """
        Evaluate likelihood score for points in the "target" list
        In this code, likelihood score (LHS) defined as
        LHS = 2*P(point) + 0.9*P(one_neighbour) + 0.8*P(2setp_neighbours)
            where P = probability of presense of a shp
        Where nibours are not available, P(point) replace P(neibours)
        Note that LHS is not probability but probability utility.
        """
        scores = []
        for i in range(len(targets)):  # i represent target number
            # Calculate LHS of target point i
            score = 0
            for row_step in range(-2, 3):
                #  Where neighbours are not available, P(point) replace P(neibours)
                if targets[i][0] + row_step in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    prob = self.enemy_probmap[targets[i][0] + row_step][targets[i][1]]
                else:
                    prob = self.enemy_probmap[targets[i][0]][targets[i][1]]
                score += (1 - 0.1 * abs(row_step)) * prob

            for col_step in range(-2, 3):
                #  Where neighbours are not available, P(point) replace P(neibours)
                if targets[i][1] + col_step in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    prob = self.enemy_probmap[targets[i][0]][targets[i][1] + col_step]
                else:
                    prob = self.enemy_probmap[targets[i][0]][targets[i][1]]
                score += (1 - 0.1 * abs(row_step)) * prob
            # Store LHS and target point i and sort at the end
            scores.append((score, i))
        scores.sort(reverse=True)

        # Return the top LSH points as list of tuple
        # The number of returning points is the same as the number of our ship
        shot_list = []
        for j in range(myship_number):
            shot_row = targets[scores[j][1]][0]
            shot_col = targets[scores[j][1]][1]
            shot_list.append((shot_row, shot_col))
        return shot_list






