import random
import numpy as np


class PathPlanning:
    def __init__(self, world_params):

        self.maxRow = world_params["maxRow"]
        self.maxCol = world_params["maxCol"]
        self.num_obstacle_pts = world_params["num_obstacle_pts"]
        self.cor_pr = world_params["cor_pr"]
        self.wr_pr = world_params["wr_pr"]
        self.n_actions = world_params["n_actions"]
        self.startRow = world_params["startRow"]
        self.startCol = world_params["startCol"]
        self.goalRow = world_params["goalRow"]
        self.goalCol = world_params["goalCol"]
        self.goalReward = world_params["goalReward"]
        self.obstReward = world_params["obstReward"]
        self.stayReward = world_params["stayReward"]
        self.gamma = world_params["gamma"]

        # Initializing model outputs

        self.not_occupied = 0
        self.oRow = []
        self.oCol = []
        self.m = np.zeros((2, self.maxRow, self.maxCol))
        self.st = np.zeros(
            (
                self.n_actions,
                self.maxRow * self.maxCol,
                self.maxRow * self.maxCol,
            )
        )
        self.num_states = self.maxRow * self.maxCol
        self.rm = np.ones((self.num_states, self.n_actions)) * self.stayReward

    def rotate(self, l, n):
        """
        rotate a list n times in anticlockwise direction
        """
        return l[n:] + l[:n]

    def get_obstacles(self):
        """
        returns a list of obstacle state indexes for rows and columns

        """

        # Getting boundaries

        # Top wall
        row = 0
        for col in range(self.maxCol):
            self.oRow.append(row)
            self.oCol.append(col)

        # Bottom wall
        row = self.maxRow - 1
        for col in range(self.maxCol):
            self.oRow.append(row)
            self.oCol.append(col)

        # Left side wall
        col = 0
        for row in range(1, self.maxRow - 1):
            self.oRow.append(row)
            self.oCol.append(col)

        # Right side wall
        col = self.maxCol - 1
        for row in range(1, self.maxRow - 1):
            self.oRow.append(row)
            self.oCol.append(col)

        # Randomly selecting obstacle states
        SameRow = 0

        # Selecting the rows
        if self.startRow < self.goalRow:

            RowRange = (
                list(range(0, self.startRow))
                + list(range(self.startRow + 1, self.goalRow))
                + list(range(self.goalRow + 1, self.maxRow - 1))
            )

        elif self.startRow > self.goalRow:

            RowRange = (
                list(range(0, self.goalRow))
                + list(range(self.goalRow + 1, self.startRow))
                + list(range(self.startRow + 1, self.maxRow - 1))
            )

        else:
            RowRange = (
                list(range(0, self.goalRow))
                + list(range(self.goalRow + 1, self.startRow))
                + list(range(self.startRow + 1, self.maxRow - 1))
            )
            SameRow = 1

        # Selecting the columns
        if self.startCol < self.goalCol:

            ColRange = (
                list(range(0, self.startCol))
                + list(range(self.startCol + 1, self.goalCol))
                + list(range(self.goalCol + 1, self.maxCol - 1))
            )

        elif self.startCol > self.goalCol:

            ColRange = (
                list(range(0, self.goalCol))
                + list(range(self.goalCol + 1, self.startCol))
                + list(range(self.startCol + 1, self.maxCol - 1))
            )

        else:

            ColRange = (
                list(range(0, self.goalCol))
                + list(range(self.goalCol + 1, self.startCol))
                + list(range(self.startCol + 1, self.maxCol - 1))
            )

            if SameRow == 1:
                raise ValueError("Start state and goal state are same")

        wallRows = [
            random.choice(RowRange) for row in range(self.num_obstacle_pts)
        ]
        wallCols = [
            random.choice(ColRange) for col in range(self.num_obstacle_pts)
        ]

        self.oRow.extend(wallRows)
        self.oCol.extend(wallCols)

        return None

    def build_map(self):
        """
        builds the map using obstacle state indexes
        """

        cur_state = 0
        for row in range(self.maxRow):
            for col in range(self.maxCol):
                self.m[0][row][col] = cur_state
                cur_state += 1

        for row, col in zip(self.oRow, self.oCol):
            if self.not_occupied == 1:

                self.m[1][row][col] = 0
            else:
                self.m[1][row][col] = 1

        return None

    def build_st_trans_matrix(self):
        """
        Function that builds state transition model for input to the MDP

        """
        if (self.cor_pr + (self.n_actions - 1) * self.wr_pr) < 0.99 or (
            self.cor_pr + (self.n_actions - 1) * self.wr_pr
        ) > 1.01:
            raise ValueError("Sum of probabilities is not close to one")

        if self.not_occupied != 0:
            if self.not_occupied != 1:
                raise ValueError("not occupied should be either zero or one")

        # Actions should start from right and go in anti clockwise direction
        for row in range(self.maxRow):
            for col in range(self.maxCol):

                cur_state = self.m[0][row][col]
                cur_occ = self.m[1][row][col]

                if cur_occ == self.not_occupied:

                    right_state = self.m[0][row][col + 1]
                    right_occ = self.m[1][row][col + 1]

                    top_state = self.m[0][row - 1][col]
                    top_occ = self.m[1][row - 1][col]

                    left_state = self.m[0][row][col - 1]
                    left_occ = self.m[1][row][col - 1]

                    bottom_state = self.m[0][row + 1][col]
                    bottom_occ = self.m[1][row + 1][col]

                    top_right_state = self.m[0][row - 1][col + 1]
                    top_right_occ = self.m[1][row - 1][col + 1]

                    top_left_state = self.m[0][row - 1][col - 1]
                    top_left_occ = self.m[1][row - 1][col - 1]

                    bottom_right_state = self.m[0][row + 1][col + 1]
                    bottom_right_occ = self.m[1][row + 1][col + 1]

                    bottom_left_state = self.m[0][row + 1][col - 1]
                    bottom_left_occ = self.m[1][row + 1][col - 1]

                    action_map = [
                        right_state,
                        top_right_state,
                        top_state,
                        top_left_state,
                        left_state,
                        bottom_left_state,
                        bottom_state,
                        bottom_right_state,
                    ]
                    occ_map = [
                        right_occ,
                        top_right_occ,
                        top_occ,
                        top_left_occ,
                        left_occ,
                        bottom_left_occ,
                        bottom_occ,
                        bottom_right_occ,
                    ]

                    for action in range(self.n_actions):

                        action_map_rot = self.rotate(action_map, action)

                        prob_sum = 0
                        for inner_action in range(self.n_actions):

                            # assign the probability of correct prob to the state in the direction of action
                            if inner_action == 0:

                                self.st[action][int(cur_state)][
                                    int(action_map_rot[inner_action])
                                ] = self.cor_pr
                                prob_sum += self.cor_pr

                            else:
                                self.st[action][int(cur_state)][
                                    int(action_map_rot[inner_action])
                                ] = self.wr_pr
                                prob_sum += self.wr_pr

        for action in range(self.n_actions):

            rowSum = np.sum(self.st[action][:][:], axis=1)
            zeroInd = np.where(rowSum == 0)[0]
            lessInd = np.where(rowSum < 1)[0]

            # Assigning probability to unreachable states so that sum of
            # each row of st matrix becomes 1
            for row in zeroInd:
                col = random.choice(range(0, self.num_states - 1))
                self.st[action][row][col] = 1

            # If the sum of probability for each row is not one
            # assigning the 1 - total probability to some random state
            for row in lessInd:
                col = random.choice(range(0, self.num_states - 1))
                self.st[action][row][col] += 1 - np.sum(self.st[action][row][:])

        return None

    def build_reward_matrix(self):
        """
        Function that builds the reward model of the world for input to the MDP for path planning

        """
        right_action = 0
        top_right_action = 1
        top_action = 2
        top_left_action = 3
        left_action = 4
        bottom_left_action = 5
        bottom_action = 6
        bottom_right_action = 7

        goal_state = self.m[0][self.goalRow][self.goalCol]
        for row in range(self.maxRow):

            for col in range(self.maxCol):

                cur_occ = self.m[1][row][col]
                if cur_occ == self.not_occupied:

                    cur_state = int(self.m[0][row][col])
                    right_state = int(self.m[0][row][col + 1])
                    top_right_state = int(self.m[0][row - 1][col + 1])
                    top_state = int(self.m[0][row - 1][col])
                    top_left_state = int(self.m[0][row - 1][col - 1])
                    left_state = int(self.m[0][row][col - 1])
                    bottom_left_state = int(self.m[0][row + 1][col - 1])
                    bottom_state = int(self.m[0][row + 1][col])
                    bottom_right_state = int(self.m[0][row + 1][col + 1])

                    right_occ = int(self.m[1][row][col + 1])
                    top_right_occ = int(self.m[1][row - 1][col + 1])
                    top_occ = int(self.m[1][row - 1][col])
                    top_left_occ = int(self.m[1][row - 1][col - 1])
                    left_occ = int(self.m[1][row][col - 1])
                    bottom_left_occ = int(self.m[1][row + 1][col - 1])
                    bottom_occ = int(self.m[1][row + 1][col])
                    bottom_right_occ = int(self.m[1][row + 1][col + 1])

                    # 1
                    if right_occ != self.not_occupied:
                        self.rm[cur_state][right_action] = self.obstReward

                    if right_state == goal_state:
                        self.rm[cur_state][right_action] = self.goalReward

                    # 2
                    if top_right_occ != self.not_occupied:
                        self.rm[cur_state][top_right_action] = self.obstReward

                    if top_right_state == goal_state:
                        self.rm[cur_state][top_right_action] = self.goalReward

                    # 3
                    if top_occ != self.not_occupied:
                        self.rm[cur_state][top_action] = self.obstReward

                    if top_state == goal_state:
                        self.rm[cur_state][top_action] = self.goalReward

                    # 4
                    if top_left_occ != self.not_occupied:
                        self.rm[cur_state][top_left_action] = self.obstReward

                    if top_left_state == goal_state:
                        self.rm[cur_state][top_left_action] = self.goalReward

                    # 5
                    if left_occ != self.not_occupied:
                        self.rm[cur_state][left_action] = self.obstReward

                    if left_state == goal_state:
                        self.rm[cur_state][left_action] = self.goalReward

                    # 6
                    if bottom_left_occ != self.not_occupied:
                        self.rm[cur_state][bottom_left_action] = self.obstReward

                    if bottom_left_state == goal_state:
                        self.rm[cur_state][bottom_left_action] = self.goalReward

                    # 6
                    if bottom_occ != self.not_occupied:
                        self.rm[cur_state][bottom_action] = self.obstReward

                    if bottom_state == goal_state:
                        self.rm[cur_state][bottom_action] = self.goalReward

                    # 8
                    if bottom_right_occ != self.not_occupied:
                        self.rm[cur_state][
                            bottom_right_action
                        ] = self.obstReward

                    if bottom_right_state == goal_state:
                        self.rm[cur_state][
                            bottom_right_action
                        ] = self.goalReward

        return None
