import json
import os

import tkinter
import threading
import numpy as np
from PIL import Image, ImageTk, ImageSequence

from model import PathPlanning
from optimizers import fit_value, fit_policy
from visualizations import plot_analysis
from utils import store_to_file


BASE_DIR = os.getcwd()
RESULTS_DIR = os.path.join(BASE_DIR, "results")
DATA_DIR = os.path.join(RESULTS_DIR, "txt_data")

os.mkdir(DATA_DIR)


def main(userInputData):
    world_params = {
        "cor_pr": 0.9,
        "wr_pr": 0.0142857,
        "n_actions": 8,
        "goalReward": 1,
        "obstReward": -15,
        "stayReward": -0.03,
        "gamma": 0.98,
    }
    world_params["maxRow"] = userInputData["maxRow"]
    world_params["maxCol"] = userInputData["maxCol"]
    world_params["num_obstacle_pts"] = userInputData["num_obstacle_pts"]
    world_params["startRow"] = userInputData["startRow"]
    world_params["startCol"] = userInputData["startCol"]
    world_params["goalRow"] = userInputData["goalRow"]
    world_params["goalCol"] = userInputData["goalCol"]
    tm = PathPlanning(world_params)
    tm.get_obstacles()
    tm.build_map()
    tm.build_st_trans_matrix()
    tm.build_reward_matrix()

    world_data = {}
    world_data["st"] = tm.st.tolist()
    world_data["rm"] = tm.rm.tolist()
    world_data["gamma"] = tm.gamma
    world_data["num_states"] = tm.num_states
    world_data["startRow"] = tm.startRow
    world_data["startCol"] = tm.startCol
    world_data["goalRow"] = tm.goalRow
    world_data["goalCol"] = tm.goalCol
    world_data["oCol"] = tm.oCol
    world_data["oRow"] = tm.oRow
    world_data["m"] = tm.m.tolist()
    world_data["maxRow"] = tm.maxRow
    world_data["maxCol"] = tm.maxCol

    os.chdir(DATA_DIR)

    print("Storing PolicyIteration data to file")
    store_to_file(world_data, "data_world.txt")

    with open("data_world.txt") as json_data:
        world_data = json.load(json_data)

    world_data["st"] = np.array(world_data["st"])
    world_data["rm"] = np.array(world_data["rm"])
    world_data["m"] = np.array(world_data["m"])

    # Policy Iteration Experimentations

    print("Experiments with Policy Iteration")

    data_policy = fit_policy(
        world_data["st"],
        world_data["rm"],
        world_data["gamma"],
        world_data["num_states"],
    )

    # Storing policy data to file
    print("Storing PolicyIteration data to file")
    store_to_file(data_policy, "data_policy.txt")

    # Value Iteration Experimentations

    print("Experiments with Value Iteration")
    data_value = fit_value(
        world_data["st"],
        world_data["rm"],
        world_data["gamma"],
        world_data["num_states"],
    )

    # Storing value data to file
    print("Storing ValueIteration data to file")
    store_to_file(data_value, "data_value.txt")

    # Showing plots
    plot_analysis(
        "data_world.txt",
        "data_value.txt",
        "data_policy.txt",
        world_params["obstReward"],
    )


def animate(canvas, root, sequence, image, counter):
    canvas.itemconfig(image, image=sequence[counter])
    root.after(
        20,
        lambda: animate(
            canvas, root, sequence, image, (counter + 1) % len(sequence)
        ),
    )


def loading():
    temp = tkinter.Tk()
    canvas = tkinter.Canvas(temp, width=400, height=400)
    canvas.pack()
    sequence = [
        ImageTk.PhotoImage(img)
        for img in ImageSequence.Iterator(Image.open(r"load.gif"))
    ]
    image = canvas.create_image(200, 200, image=sequence[0])
    animate(canvas, temp, sequence, image, 1)
    temp.mainloop()


def threader(userinputData):
    t1 = threading.Thread(target=loading)
    t2 = threading.Thread(target=main, args=(userinputData,))
    t2.start()
    t1.start()
