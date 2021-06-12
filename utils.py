import json


def get_reward(
    startRow,
    startCol,
    goalRow,
    goalCol,
    num_states,
    m,
    optimal_policy,
    rm,
    maxRow,
    maxCol,
):
    """
    Function to count the total reward

    """

    cur_row = startRow
    cur_col = startCol

    opt_row = [startRow]
    opt_col = [startCol]
    max_points = num_states
    cur_point = 0

    total_reward = 0

    while 1:
        new_row = 0
        new_col = 0
        cur_state = int(m[0][cur_row][cur_col])

        cur_opt_action = optimal_policy[str(cur_state)]
        total_reward += rm[cur_state][cur_opt_action]

        # right
        if cur_opt_action == 0:
            new_row = cur_row
            new_col = cur_col + 1
        # top-right
        elif cur_opt_action == 1:
            new_row = cur_row - 1
            new_col = cur_col + 1
        # top
        elif cur_opt_action == 2:
            new_row = cur_row - 1
            new_col = cur_col
        # top-left
        elif cur_opt_action == 3:
            new_row = cur_row - 1
            new_col = cur_col - 1
        # left
        elif cur_opt_action == 4:
            new_row = cur_row
            new_col = cur_col - 1
        # bottom-left
        elif cur_opt_action == 5:
            new_row = cur_row + 1
            new_col = cur_col - 1
        # bottom
        elif cur_opt_action == 6:
            new_row = cur_row + 1
            new_col = cur_col
        # bottom-right
        else:
            new_row = cur_row + 1
            new_col = cur_col + 1

        if new_row > maxRow - 1 or new_col > maxCol - 1:
            break
        else:
            cur_row = new_row
            cur_col = new_col

        opt_row.append(cur_row)
        opt_col.append(cur_col)

        cur_point += 1
        if cur_row == goalRow:
            if cur_col == goalCol:
                print("Goal Reached!!")
                break

        if cur_point == max_points:
            print("Steps limit over!!")
            break

    return total_reward


def store_to_file(data, file_name):
    with open(file_name, "w") as outfile:
        json.dump(data, outfile)