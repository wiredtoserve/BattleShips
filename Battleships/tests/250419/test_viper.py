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

        # number of turns
        self.counter = 0

        self.positions = None  # store indexes for ships

    def setup_ships(self):
        '''

        :return: a 10x10 grid with the location of our ships
        '''
        grid = [[0 for i in range(10)] for j in range(10)]

        self.init_position()
        while self.is_good_position() == False:
            self.init_position()
            self.is_good_position()

        # update postion index to myport
        points = self.positions
        points_len = len(points)
        i = 0
        while i < points_len:
            for item in points[i]:
                row = item[0]
                col = item[1]
                grid[row][col] = i + 1
            i += 1

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

        # last_shot = history[-1]['incoming'] if self.counter > 0 else []

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

        # previous_shots = history[-1]['shots'] if self.counter > 0 else []

        self.enemyport = self.update_enemy_map(self.enemyport, previous_shots)

        # Based on some logic here, choose to shoot
        # using probability

        shots_list = self.shot(history, number_of_ships, last_shot)

        # update the number of turns
        self.counter += 1

        return shots_list

    def get_name(self):
        '''

        :return: string - name of the Player
        '''
        return "Syndicate_10"

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
    def shot(self, history, myship_number, last_shot):
        """ decide target area based on the number of enemy ships"""
        try:
            if (len(history) <= 1 or len(last_shot) == 5) and (len(history) <= 5):
                row_range = range(6)
                column_range = range(6)
            elif len(last_shot) == 4 and len(history) <= 12:
                row_range = range(4, 10)
                column_range = range(4, 10)
            elif len(last_shot) == 3 and len(history) <= 15:
                row_range = range(5)
                column_range = range(6, 10)
            elif len(last_shot) == 2 and len(history) <= 15:
                row_range = range(6, 10)
                column_range = range(5)
            else:
                row_range = range(10)
                column_range = range(10)
        except Exception as e:
            row_range = range(6)
            column_range = range(6)


        """
        Store the "coordinates of spots that have not been shot"
        into the list called "targets" and shuffle them to add randomness
        """
        targets = []
        try:
            for row in row_range:
                for column in column_range:
                    if self.enemyport[row][column] == 0:
                        targets.append((row, column))
        except Exception as e:
            for row in range(10):
                for column in range(10):
                    if self.enemyport[row][column] == 0:
                        targets.append((row, column))
        Player.random.shuffle(targets)
        """
        Evaluate likelihood score for points in the "target" list
        In this code, likelihood score (LHS) defined as
        LHS = 2*P(point) + 0.9*P(one_neighbour) + 0.8*P(2 step_neighbours)
            where P = expected probability of a shp
        Where neighbours are not available, P(point) replace P(one_neighbour)
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
                score += (1 - 0.1 * abs(col_step)) * prob
            # Store LHS and target point i and sort at the end
            scores.append((score, i))
        scores.sort(reverse=True)

        # Return the top LSH points as list of tuple
        # The number of returning points is the same as the number of our ship
        shot_list = []
        for j in range(myship_number):
            if j <= len(targets) - 1:
                shot_row = targets[scores[j][1]][0]
                shot_col = targets[scores[j][1]][1]
            else:
                shot_row = targets[-1][0]
                shot_col = targets[-1][1]
            shot_list.append((shot_row, shot_col))
        return shot_list

    """ is good placing strategy if ships don't touch"""

    def is_good_position(self):
        points = self.positions
        signal = True
        points_len = len(points)
        for ship in points:
            position = points.index(ship)
            length = len(ship)
            # get two end points for the ship
            end = None
            if length == 1:
                end = ship
            else:
                end = [ship[0], ship[length - 1]]

            # check if end points touch any other ship points:
            i = position + 1
            while i < points_len:
                another_ship = points[i]
                for stuff in another_ship:
                    for item in end:
                        if (stuff[0] == item[0]) and (abs(stuff[1] - item[1])) == 2:
                            return False
                        elif (stuff[1] == item[1]) and (abs(stuff[0] - item[0])) == 2:
                            return False
                        else:
                            signal = True

                i += 1

        return signal

    def init_position(self):  # initiate potential positions to place ships
        """strategy is divide myport our 5*5 area so every area will contain at most 2 ships"""

        # the direction ships point : 0 - down; 1- right
        row_range = {1: (0, 5), 2: (0, 5), 3: (5, 10), 4: (5, 10)}  # store row index range for different areas
        col_range = {1: (0, 5), 2: (5, 10), 3: (0, 5), 4: (5, 10)}  # store col index range for different areas

        # always place 1 and 2 together so the distribution is even
        area_order = Player.random.sample(range(1, 5), 4)  # areas are labeled 1,2,3,4, this one generate an order

        # For ship 1 and 2 in area i
        area = area_order[0]
        row_edge = row_range[area]
        col_edge = col_range[area]
        row_1 = Player.random.sample(range(row_edge[0], row_edge[1]), 1)[0]
        col_1 = Player.random.sample(range(col_edge[0], col_edge[1]), 1)[0]
        points = [[(row_1, col_1)]]  # get the position for ship 1

        # get the position for ship 2
        while True:
            dirt = Player.random.randint(0, 1)
            if dirt == 0:  # down
                row_2 = Player.random.sample(range(row_edge[0], row_edge[1] - 1), 1)[0]
                col_2 = Player.random.sample(range(col_edge[0], col_edge[1]), 1)[0]
                points_2 = [(row_2, col_2), (row_2 + 1, col_2)]
                if points[0][0] not in points_2:
                    points.append(points_2)

                    break

            else:  # right
                row_2 = Player.random.sample(range(row_edge[0], row_edge[1]), 1)[0]
                col_2 = Player.random.sample(range(col_edge[0], col_edge[1] - 1), 1)[0]
                points_2 = [(row_2, col_2), (row_2, col_2 + 1)]
                if points[0][0] not in points_2:
                    points.append(points_2)

                    break

        # For ship 3,4,5 in different areas:
        i = 3
        while i <= 5:
            area = area_order[i - 2]
            row_edge = row_range[area]
            col_edge = col_range[area]

            dirt = Player.random.randint(0, 1)
            if dirt == 0:  # down
                row_i = Player.random.sample(range(row_edge[0], row_edge[1] - i + 1), 1)[0]
                col_i = Player.random.sample(range(col_edge[0], col_edge[1]), 1)[0]
                points_i = [(row_i, col_i)]
                j = 1
                while j < i:
                    points_i.append((row_i + j, col_i))
                    j += 1

            else:  # right
                row_i = Player.random.sample(range(row_edge[0], row_edge[1]), 1)[0]
                col_i = Player.random.sample(range(col_edge[0], col_edge[1] - i + 1), 1)[0]
                points_i = [(row_i, col_i)]
                j = 1
                while j < i:
                    points_i.append((row_i, col_i + j))
                    j += 1
            points.append(points_i)
            i += 1

        self.positions = points
        return None
