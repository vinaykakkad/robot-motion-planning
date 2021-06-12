import os
import json
import matplotlib.pyplot as plt

from utils import get_reward


BASE_DIR = os.getcwd()
RESULTS_DIR = os.path.join(BASE_DIR, "results")
PATH_DIR = os.path.join(RESULTS_DIR, "optimal_paths")
POLICY_DIR = os.path.join(RESULTS_DIR, "optimal_policies")
REWARDS_DIR = os.path.join(RESULTS_DIR, "rewards")
TIME_DIR = os.path.join(RESULTS_DIR, "time")

os.mkdir(RESULTS_DIR)
os.mkdir(PATH_DIR)
os.mkdir(POLICY_DIR)
os.mkdir(REWARDS_DIR)
os.mkdir(TIME_DIR)


def visualize_path(
    startRow,
    startCol,
    goalRow,
    goalCol,
    oCol,
    oRow,
    num_states,
    m,
    optimal_policy,
    algorithm,
):
    # Visualize world
    fig, ax = plt.subplots(figsize=(12, 12))
    plt.ion()
    ax.scatter(oCol, oRow, marker="s", s=700, c="black")
    ax.scatter(startCol, startRow, s=700, c="b")
    ax.scatter(goalCol, goalRow, s=700, c="g")
    plt.axis("equal")
    plt.axis("tight")

    os.chdir(RESULTS_DIR)
    fig.savefig("map.png")

    # Visualize path
    cur_row = startRow
    cur_col = startCol

    opt_row = [startRow]
    opt_col = [startCol]
    max_points = num_states
    cur_point = 0

    # print('current state  row: {}, col: {}'.format(self.startRow, self.startCol))
    while 1:

        cur_state = int(m[0][cur_row][cur_col])
        cur_opt_action = optimal_policy[str(cur_state)]

        # right
        if cur_opt_action == 0:
            cur_row = cur_row
            cur_col = cur_col + 1
        # top-right
        elif cur_opt_action == 1:
            cur_row = cur_row - 1
            cur_col = cur_col + 1
        # top
        elif cur_opt_action == 2:
            cur_row = cur_row - 1
            cur_col = cur_col
        # top-left
        elif cur_opt_action == 3:
            cur_row = cur_row - 1
            cur_col = cur_col - 1
        # left
        elif cur_opt_action == 4:
            cur_row = cur_row
            cur_col = cur_col - 1
        # bottom-left
        elif cur_opt_action == 5:
            cur_row = cur_row + 1
            cur_col = cur_col - 1
        # bottom
        elif cur_opt_action == 6:
            cur_row = cur_row + 1
            cur_col = cur_col
        # bottom-right
        else:
            cur_row = cur_row + 1
            cur_col = cur_col + 1

        opt_row.append(cur_row)
        opt_col.append(cur_col)

        ax.plot(opt_col, opt_row, linewidth=5, color="red")

        cur_point += 1

        if cur_row == goalRow:
            if cur_col == goalCol:
                print("Goal Reached!!")
                break

        if cur_point == max_points:
            print("Steps limit over!!")
            break

    os.chdir(PATH_DIR)
    figname = f"optimal_path_{algorithm}"
    fig.savefig(figname)
    plt.close()


def visualize_policy(
    maxRow,
    maxCol,
    startRow,
    startCol,
    goalRow,
    goalCol,
    oCol,
    oRow,
    num_states,
    m,
    optimal_policy,
    algorithm,
):
    # Visualize world
    fig, ax = plt.subplots(figsize=(5.8, 5.8))
    plt.ion()
    ax.scatter(oCol, oRow, marker="s", s=700, c="black")
    ax.scatter(startCol, startRow, s=700, c="b")
    ax.scatter(goalCol, goalRow, s=700, c="g")
    plt.axis("equal")
    plt.axis("tight")

    # Arrow config
    arrow_head_len = 0.1
    len_arrow = 1 - 2 * arrow_head_len
    arrow = {}
    arrow["right"] = {
        "sx": -1 * (len_arrow / 2),
        "sy": 0,
        "dx": len_arrow,
        "dy": 0,
    }
    arrow["top"] = {
        "sx": 0,
        "sy": (len_arrow / 2),
        "dx": 0,
        "dy": -1 * len_arrow,
    }
    arrow["left"] = {
        "sx": (len_arrow / 2),
        "sy": 0,
        "dx": -1 * len_arrow,
        "dy": 0,
    }
    arrow["bottom"] = {
        "sx": 0,
        "sy": -1 * (len_arrow / 2),
        "dx": 0,
        "dy": len_arrow,
    }
    arrow["bottom_right"] = {
        "sx": -1 * (len_arrow / 2),
        "sy": -1 * (len_arrow / 2),
        "dx": len_arrow,
        "dy": len_arrow,
    }
    arrow["bottom_left"] = {
        "sx": (len_arrow / 2),
        "sy": -1 * (len_arrow / 2),
        "dx": -1 * len_arrow,
        "dy": len_arrow,
    }
    arrow["top_left"] = {
        "sx": (len_arrow / 2),
        "sy": (len_arrow / 2),
        "dx": -1 * len_arrow,
        "dy": -1 * len_arrow,
    }
    arrow["top_right"] = {
        "sx": -1 * (len_arrow / 2),
        "sy": (len_arrow / 2),
        "dx": len_arrow,
        "dy": -1 * len_arrow,
    }

    # Visualize path
    cur_row = startRow
    cur_col = startCol

    merged_list = [(oRow[i], oCol[i]) for i in range(0, len(oRow))]
    # print('current state  row: {}, col: {}'.format(self.startRow, self.startCol))
    for cur_row in range(maxRow):
        for cur_col in range(maxCol):
            curr_loc = (cur_row, cur_col)
            cur_state = int(m[0][cur_row][cur_col])
            cur_opt_action = optimal_policy[str(cur_state)]

            if cur_opt_action == 0:
                direction = "right"
                x = arrow[direction]["sx"] + cur_col
                y = arrow[direction]["sy"] + cur_row
                dx = arrow[direction]["dx"]
                dy = arrow[direction]["dy"]

            elif cur_opt_action == 1:
                direction = "top_right"
                x = arrow[direction]["sx"] + cur_col
                y = arrow[direction]["sy"] + cur_row
                dx = arrow[direction]["dx"]
                dy = arrow[direction]["dy"]

            elif cur_opt_action == 2:
                direction = "top"
                x = arrow[direction]["sx"] + cur_col
                y = arrow[direction]["sy"] + cur_row
                dx = arrow[direction]["dx"]
                dy = arrow[direction]["dy"]

            elif cur_opt_action == 3:
                direction = "top_left"
                x = arrow[direction]["sx"] + cur_col
                y = arrow[direction]["sy"] + cur_row
                dx = arrow[direction]["dx"]
                dy = arrow[direction]["dy"]

            elif cur_opt_action == 4:
                direction = "left"
                x = arrow[direction]["sx"] + cur_col
                y = arrow[direction]["sy"] + cur_row
                dx = arrow[direction]["dx"]
                dy = arrow[direction]["dy"]

            elif cur_opt_action == 5:
                direction = "bottom_left"
                x = arrow[direction]["sx"] + cur_col
                y = arrow[direction]["sy"] + cur_row
                dx = arrow[direction]["dx"]
                dy = arrow[direction]["dy"]

            elif cur_opt_action == 6:
                direction = "bottom"
                x = arrow[direction]["sx"] + cur_col
                y = arrow[direction]["sy"] + cur_row
                dx = arrow[direction]["dx"]
                dy = arrow[direction]["dy"]

            else:
                direction = "bottom_right"
                x = arrow[direction]["sx"] + cur_col
                y = arrow[direction]["sy"] + cur_row
                dx = arrow[direction]["dx"]
                dy = arrow[direction]["dy"]

            if curr_loc in merged_list:
                ax.arrow(
                    x,
                    y,
                    dx,
                    dy,
                    head_width=0.3,
                    head_length=0.1,
                    fc="red",
                    ec="red",
                )
            else:
                ax.arrow(
                    x,
                    y,
                    dx,
                    dy,
                    head_width=0.3,
                    head_length=0.1,
                    fc="green",
                    ec="green",
                )

    os.chdir(POLICY_DIR)
    figname = "optimal_policy_" + algorithm
    fig.savefig(figname)
    plt.close()


def plot_analysis(
    file_data_world,
    file_data_value,
    file_data_policy,
    obstReward,
):
    iterations = list(range(1, 1000, 10))
    with open(file_data_world) as json_data:
        data_world = json.load(json_data)

    with open(file_data_value) as json_data:
        data_value = json.load(json_data)

    with open(file_data_policy) as json_data:
        data_policy = json.load(json_data)

    # Total computation time
    tot_time_policy = []
    tot_time_value = []
    for iter in iterations:
        tot_time_policy.append(data_policy[str(iter)]["tot_time"])
        tot_time_value.append(data_value[str(iter)]["tot_time"])

    fig, ax = plt.subplots()
    ax.plot(iterations, tot_time_policy)
    ax.plot(iterations, tot_time_value)
    plt.legend(["PolicyIteration", "ValueIteration"])
    plt.title("Total computation time (s)")
    plt.ylabel("Time in seconds")
    plt.xlabel("Iterations")
    os.chdir(TIME_DIR)
    fig.savefig("total_time.png")

    # Average value update time
    value_time_policy = []
    value_time_value = []

    for itr in iterations:

        time_policy = []
        for time_value in data_policy[str(itr)]["time_iter"]:
            time_policy.append(sum(time_value) / float(len(time_value)))

        value_time_policy.append(sum(time_policy) / len(time_policy))
        value_time_value.append(
            sum(data_value[str(itr)]["time_iter"])
            / len(data_value[str(itr)]["time_iter"])
        )

    fig2, ax2 = plt.subplots()
    ax2.plot(iterations, value_time_policy)
    ax2.plot(iterations, value_time_value)
    ax2.legend(["PolicyIteration", "ValueIteration"])
    plt.title("Average time of per value update iteration")
    plt.ylabel("Time in seconds")
    plt.xlabel("Iterations")
    fig2.savefig("value_time.png")

    # Visualize path and policy for policy iteration and value iteration
    visualize_policy(
        data_world["maxRow"],
        data_world["maxCol"],
        data_world["startRow"],
        data_world["startCol"],
        data_world["goalRow"],
        data_world["goalCol"],
        data_world["oCol"],
        data_world["oRow"],
        data_world["num_states"],
        data_world["m"],
        data_policy["convergence"]["optimal_policy"],
        "policy_iteration",
    )
    visualize_path(
        data_world["startRow"],
        data_world["startCol"],
        data_world["goalRow"],
        data_world["goalCol"],
        data_world["oCol"],
        data_world["oRow"],
        data_world["num_states"],
        data_world["m"],
        data_policy["convergence"]["optimal_policy"],
        "policy_iteration",
    )
    visualize_path(
        data_world["startRow"],
        data_world["startCol"],
        data_world["goalRow"],
        data_world["goalCol"],
        data_world["oCol"],
        data_world["oRow"],
        data_world["num_states"],
        data_world["m"],
        data_value["convergence"]["optimal_policy"],
        "value_iteration",
    )

    visualize_policy(
        data_world["maxRow"],
        data_world["maxCol"],
        data_world["startRow"],
        data_world["startCol"],
        data_world["goalRow"],
        data_world["goalCol"],
        data_world["oCol"],
        data_world["oRow"],
        data_world["num_states"],
        data_world["m"],
        data_value["convergence"]["optimal_policy"],
        "value_iteration",
    )

    # Calculating reward
    policy_policy = data_policy["convergence"]["policies"]
    policy_value = data_value["convergence"]["policies"]

    print(len(policy_policy))
    print(len(policy_value))
    reward_policy = []
    reward_value = []
    for p_pol in policy_policy:
        reward_p = get_reward(
            data_world["startRow"],
            data_world["startCol"],
            data_world["goalRow"],
            data_world["goalCol"],
            data_world["num_states"],
            data_world["m"],
            p_pol,
            data_world["rm"],
            data_world["maxRow"],
            data_world["maxCol"],
        )
        reward_policy.append(reward_p)

    for v_pol in policy_value:
        reward_v = get_reward(
            data_world["startRow"],
            data_world["startCol"],
            data_world["goalRow"],
            data_world["goalCol"],
            data_world["num_states"],
            data_world["m"],
            v_pol,
            data_world["rm"],
            data_world["maxRow"],
            data_world["maxCol"],
        )
        reward_value.append(reward_v)

    fig3, ax3 = plt.subplots(figsize=(5, 4))
    ax3.plot(list(range(len(reward_policy))), reward_policy)
    plt.xlabel("iterations")
    plt.ylabel("reward collected")
    plt.title("Policy Iteration")
    os.chdir(REWARDS_DIR)
    fig3.savefig("reward_policy.png")

    fig4, ax4 = plt.subplots(figsize=(5, 4))
    ax4.plot(list(range(len(reward_value)))[1:100], reward_value[1:100])
    plt.xlabel("iterations")
    plt.ylabel("reward collected")
    plt.title("Value Iteration")
    fig4.savefig("reward_value.png")
