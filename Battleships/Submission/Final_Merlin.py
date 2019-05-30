class Player:
    """
    Syndicate 10 Submission
    Contains three methods
        1. setup_ships: takes no parameters and returns a list of lists showing the start position
                        of showing the start positions of your ships
                        Block of row i and column j, ship label 1-5 & 0 means no ship

        2. take_turn:   returns
                        -- a list of (row, column) tuples describing your shots
                        -- Note: should be equal to the number of ships present
                        -- or a tuple that has a ship number as the first element and the direction
                        -- of its moving value
                        -- 0: up, 1: right, 2: down, 3: left

        3. get_name:   returns a string that is the name of the Player

    """
    import random
    from collections import defaultdict

    def __init__(self):
        '''
        Following variables are initiated when a class is instantiated
        self.player_battleground: representation of the player's map
        self.ships_dd           : default dictionary that counts the unique numbers in the map
        self.status             : a list of tuples that contains each ship number with its current status
                                    eg: [(5, 0.20)] is ship 5 with 20% remainin
        self.enemyport          : representation of the enemy's map. will record player's attact point
        self.enemy_probmap      : probability of enemy ship presence in each grid point 
        self.counter            : a predefined counter that keeps track of the turns
        self.hits_by_player     : a running total number of shots fired by the player
        self.positions          : store indexes for ships
        '''
        self.player_battleground = [[0 for i in range(10)] for j in range(10)]
        self.ships_dd = Player.defaultdict(int)
        self.status = []
        self.enemyport = [[0 for i in range(10)] for j in range(10)]
        self.enemy_probmap = [[15 for i in range(10)] for j in range(10)]
        self.counter = 0
        self.hits_by_player = 0
        self.positions = None

    def setup_ships(self):
        '''
        Mandatory function that optimizes the locations on the Players ships
        placed on the 10x10 grid
        It initializes a position for the ships in different areas of the map
        Ships are weighed linearly by their size
        Ships 1 and 2 are placed together, Ships 3, 4 and 5 are placed in the
        other regions
        Once the threshold criteria is met, it assigns the ships in those regions
        :return: a 10x10 grid with the location of our ships
        '''
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
                self.player_battleground[row][col] = i + 1
            i += 1
        return self.player_battleground

    def take_turn(self, history):
        '''
        The take turn function dictates the overall strategy of the player
        It keeps count of the number of turns the player has taken by updating a counter
        every time the function is called
            1. First it updates the players grid with the list on incoming shots
            2. Based on that it calculates the status of the ships hit and the number of ships that
               are currently present
            3. It then updates the opponents grid by marking the places that the player has shot
            4. Based on this history, the number of shots, the placement of them and the number of hits
               it dynamically creates a probability map to determine the best positions to shoot next
            5. The Player then shoots according to the number of ships it has present
            6. The Player does not move as it tries to maximize its chances of winning by trying to shoot
                as many number of times it can

        :param history: records the game
                        list that contains one entry per turn
                        dict with 3 keys
                            - 'shots' : list of shots made in the turn
                            - 'hits' : an integer number of hits that your shots made
                            - 'incoming' : opponents list of shots, [] if moved

        :return: a list of tuple/s named "shots_list" describing the shots or changed location
                depending on the strategy
        '''

        last_shot = []
        # updating the enemy port
        previous_shots = []
        if self.counter > 0:
            last_shot = history[-1]['incoming']
            previous_shots = history[-1]['shots']

        self.player_battleground = self.update_opponent_shots(self.player_battleground, last_shot)

        # counting the number of ships left
        self.ships_dd = Player.defaultdict(int)  # reset count every time

        # returns the dict with the number of ships and hits
        for row in self.player_battleground:
            for point in row:
                self.ships_dd[point] += point

        self.status = self.ship_status(self.ships_dd)

        # Count the number of ships remaining
        number_of_ships = len(self.status)

        # Updating the opponent map and probability matrix
        self.update_enemy_map(previous_shots)
        self.update_enemy_probmap(history)

        # Choose to shoot based on the current status in the game
        shots_list = self.shot(number_of_ships)

        # update the number of turns
        self.counter += 1

        return shots_list

    def get_name(self):
        '''
        :return: string - name of the Player
        '''
        return "Syndicate_10"

    # function to update the player battleground with the incoming shots
    def update_opponent_shots(self, grid, incoming_shots):
        '''
        Keeps track of the shots that the opponent has made on the players grid
        If the opponent has shot, then it updates the corresponding locations in
        the grid by 9
        :param grid: the players grid with the ships placed and the current status
        :param incoming_shots: the shots that the opponent has made, gathered from history
        :return: the updated player grid marked with '9' for the shots placed
        '''
        if incoming_shots:
            for x, y in incoming_shots:
                grid[x][y] = 9
        return grid

    # function that counts the number of ships and her ports hit
    def ship_status(self, ships_dd):
        '''
        :param ships_dd: a default dictionary that counts the frequencies of the number on the map
        :return: a list of tuples with the ship numbers and its status
        '''
        status = []
        for ship in ships_dd.keys():
            # as long as the default dictionary has a key, the ship is breathing
            if ship in [1, 2, 3, 4, 5]:
                status.append((ship, ships_dd[ship] / (ship ** 2)))
        return status

    def update_enemy_probmap(self, history):
        '''
        "update_enemy_probmap Function"
        - calculate probability of enemy ship presence in each grid point
        - The input for the functions is "history"
        '''
        # reset enemy_probmap with -1 for all grid
        self.enemy_probmap = [[-1 for i in range(10)] for j in range(10)]

        total_hit = 0
        total_shot = 0
        for turn in history:
            # record the success rate of each shot in enemy_probmap
            if len(turn['shots']) != 0:
                prob = turn['hits'] / len(turn['shots']) * 100
                for i in turn['shots']:
                    self.enemy_probmap[i[0]][i[1]] = prob
            total_hit += turn['hits']
            total_shot += len(turn['shots'])

        # update the probablity of spots that have not been shot.
        prob = (15 - total_hit) / (100 - total_shot) * 100 + 0.5
        for row in range(10):
            for column in range(10):
                if self.enemy_probmap[row][column] == -1:
                    self.enemy_probmap[row][column] = prob

        # multiply probability of each grid by the weight which depends on gird location
        # the grids in the center of the map have higher weights
        for row in range(10):
            for column in range(10):
                if (row, column) in [(0, 0), (9, 9), (9, 0), (0, 9)]:
                    weight = 15 / 15
                elif (row, column) in [(1, 0), (0, 1), (8, 0), (1, 9), (0, 8), (9, 1), (8, 9), (9, 8)]:
                    weight = 16.5 / 15
                elif (row, column) in [(1, 1), (1, 8), (8, 1), (8, 8)]:
                    weight = 18 / 15
                elif (row in [0, 9] and 2 <= column <= 7) or (column in [0, 9] and 2 <= row <= 7):
                    weight = 18 / 15
                elif (row in [1, 8] and 2 <= column <= 7) or (column in [1, 8] and 2 <= row <= 7):
                    weight = 19.5 / 15
                else:
                    weight = 21 / 15
                self.enemy_probmap[row][column] = weight * self.enemy_probmap[row][column]

    def update_enemy_map(self, previous_shots):
        '''
        "update_enemy_map Function"
        - Mark '9' on the enemy map, recording the points we made shot
        - The input for the functions is  "coordinate of previous_shots "
        '''
        # check if the player shot or moved in the previous shot
        if type(previous_shots) == type([]):
            if previous_shots:
                for x, y in previous_shots:
                    self.enemyport[x][y] = 9
                    # add to the total number of hits
                    self.hits_by_player += 1

    def shot(self, myship_number):
        '''
        "shot Function"
        - Generate a list of shots (coordinates of attack points)
        - The input for the functions is "number of ship we have"
        Within the target area, store the "coordinates of spots that have not been shot"
        into the list called "targets" and shuffle them to add randomness'''
        targets = []
        for row in range(10):
            for column in range(10):
                if self.enemyport[row][column] == 0:
                    targets.append((row, column))
        Player.random.shuffle(targets)

        '''
        Evaluate likelihood score for points in the "target" list
        In this code, likelihood score (LHS) defined as
        LHS = 2*P(point) + 0.9*P(one_neighbour) + 0.8*P(2 step_neighbours)
            where P = expected probability of a shp
        Where neighbours are not available, P(one_neighbour of other side) will be used
        Note that LHS is not probability but probability utility.
        Store LHS and target point i and sort at the end'''
        valid_grid = range(10)
        scores = []
        for i in range(len(targets)):  # i represent target number
            # Calculate LHS of target point i
            score = 0
            for step in range(-2, 3):
                # row weighted probability summation
                if targets[i][0] + step in valid_grid:
                    row_prob = self.enemy_probmap[targets[i][0] + step][targets[i][1]]
                else:
                    row_prob = self.enemy_probmap[targets[i][0] - step][targets[i][1]]
                score += (1 - 0.1 * abs(step)) * row_prob
                # column weighted probability summation
                if targets[i][1] + step in valid_grid:
                    column_prob = self.enemy_probmap[targets[i][0]][targets[i][1] + step]
                else:
                    column_prob = self.enemy_probmap[targets[i][0]][targets[i][1] - step]
                score += (1 - 0.1 * abs(step)) * column_prob
            scores.append((score, i))
        scores.sort(reverse=True)

        # Return the top LSH score as list of tuple
        # The number of returning points is the same as the number of our ship
        shot_list = []
        for j in range(myship_number):
            if j <= len(targets) - 1:
                shot_row = targets[scores[j][1]][0]
                shot_col = targets[scores[j][1]][1]
                shot_list.append((shot_row, shot_col))
        return shot_list

    def is_good_position(self):
        """
        : function check if initial positions are good
        is good placing strategy if ships dont touch

        :return: boolean, true if is a good ship placing strategy,
        false other wise.
        """
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
        """
        function to generate positions to place ships
        strategy is divide the playground to four 5*5 areas
        so every area will contain at most 2 ships
        It then updates the positions
        """

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
            # decide the ship placment direction.
            direction = Player.random.randint(0, 1)  
            if direction == 0:  # down
                row_2 = Player.random.sample(range(row_edge[0], row_edge[1] - 1), 1)[0]
                col_2 = Player.random.sample(range(col_edge[0], col_edge[1]), 1)[0]
                points_2 = [(row_2, col_2), (row_2 + 1, col_2)]

            else:  # right
                row_2 = Player.random.sample(range(row_edge[0], row_edge[1]), 1)[0]
                col_2 = Player.random.sample(range(col_edge[0], col_edge[1] - 1), 1)[0]
                points_2 = [(row_2, col_2), (row_2, col_2 + 1)]
               
            if points[0][0] not in points_2:
                points.append(points_2)
                break

        # For ship 3,4,5 in different areas, index 'i' is ship number:
        i = 3
        while i <= 5:
            area = area_order[i - 2]
            row_edge = row_range[area]
            col_edge = col_range[area]
            # decide the ship placment direction.
            direction = Player.random.randint(0, 1)
            if direction == 0:  # down
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