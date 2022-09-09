import logging
import json
import matplotlib.pyplot as plt
import numpy as np
import random

from AStar import AStar
from Colors import Colors
from Grid import Grid
from Logger import Logger
from Node import Node
from Obstacle import Obstacle
from Plot import Plot
from RRT import RRT

def read_scenario(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)

def read_obstacles(path: str) -> list[Obstacle]:
    obstacles: list[Obstacle] = []
    with open(path, "r") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                continue
            x, y = line.split(",")
            obstacles.append(
                Obstacle(
                    x=float(x),
                    y=float(y),
                    radius=0.5
                )
            )
    return obstacles

def problem_2() -> None:

    bot_radius: float = 0.49
    grid: Grid = Grid(
        grid_spacing=0.5,
        min_x=0,
        max_x=50,
        min_y=0,
        max_y=50,
        obstacles=read_obstacles("HW3/obstacles/biggrids.csv"),
    )

    start = Node(x=49, y=0.5)
    goal = Node(x=0.5, y=49)

    grid.inflate_bounds(bot_radius)
    # grid.inflate_obstacles(bot_radius)

    a_star: AStar = AStar(
        grid=grid,
        start=start,
        goal=goal,
    )
    a_star.find_path()

    # PLOT
    fig, ax = plt.subplots()
    ax.set_title(
        f"A*\n" \
        f"do_diagnoals={a_star.do_diagonals}, " \
        f"grid_spacing={grid.grid_spacing:.2f}m,\n" \
        f"bot_radius={bot_radius:.2f}m, " \
        f"ellapsed_time={a_star.timings['find_path'].total:.2f} sec." \
    )
    ax.set_ylabel("Y (m)")
    ax.set_xlabel("X (m)")
    
    ax.set_xlim(grid.min_x - grid.grid_spacing, grid.max_x + grid.grid_spacing)
    ax.set_ylim(grid.min_y - grid.grid_spacing, grid.max_y + grid.grid_spacing)

    a_star.plot_visited_nodes(ax, color=Colors.light_grey)
    grid.plot_obstacles(ax, Colors.red)

    # plot start and goal
    ax.plot(start.x, start.y, "o", color=Colors.green)
    ax.plot(goal.x, goal.y, "o", color=Colors.white)

    # plot path

    Plot.plot_animation(fig, ax, animate=False, save_animation=True)

def problem_3() -> None:
    scenario: dict = read_scenario("HW3/scenarios/2.json")
    grid: Grid = Grid(
        min_x=scenario["x_bounds"][0],
        max_x=scenario["x_bounds"][1],
        min_y=scenario["y_bounds"][0],
        max_y=scenario["y_bounds"][1],
        grid_spacing=scenario["grid_spacing"],
        obstacles=read_obstacles(scenario["obstacles"]),
    )

    start =  Node(x=scenario["start"][0], y=scenario["start"][1])
    goal = Node(x=scenario["goal"][0], y=scenario["goal"][1])
    bot_radius: float = scenario["bot_radius"]
    step_length: float = scenario["step_length"]
    
    grid.inflate_bounds(bot_radius)
    # grid.inflate_obstacles(bot_radius)

    rrt: RRT = RRT(
        step_length=scenario["step_length"],
        start=start, 
        goal=goal, 
        grid=grid
    )
    rrt.find_path()

    fig, ax = plt.subplots()
    fig.patch.set_facecolor(Colors.grey)
    ax.set_facecolor(Colors.grey)
    ax.title.set_color(Colors.light_grey)
    ax.xaxis.label.set_color(Colors.light_grey)
    ax.yaxis.label.set_color(Colors.light_grey)
    ax.tick_params(axis='x', colors=Colors.light_grey)
    ax.tick_params(axis='y', colors=Colors.light_grey)

    # plot start and goal
    ax.plot(start.x, start.y, "o", color=Colors.green)
    ax.plot(goal.x, goal.y, "o", color=Colors.white)
    
    ax.set_xlim(grid.min_x - grid.grid_spacing, grid.max_x + grid.grid_spacing)
    ax.set_ylim(grid.min_y - grid.grid_spacing, grid.max_y + grid.grid_spacing)

    grid.plot_obstacles(ax, color=Colors.red)
    rrt.plot_path(ax, Colors.light_blue)

    plt.show()


def for_fun() -> None:
    """
    The for_fun function generates a random number and size of obstacles and a 
    random start-goal combinations. It forces the goal to be in the bottom right, and the start
    to be in the top left. It does this as many times as necessary until it creates
    a valid map (one that has a path and is of minimum defined distance).
    """
    # generate a seed
    seed = random.randint(0, 99999)  # 5 digit cause I can't be asked to type in more
    # seed = 12345
    random.seed(seed)
    logging.info(f"Seed: {seed}")

    # setting bot radius
    bot_radius: float = 0.5

    # setting grid
    grid: Grid = Grid(
        grid_spacing=0.5,
        min_x=0,
        max_x=10,
        min_y=0,
        max_y=10,
        obstacles=[]
    )
    grid.inflate_bounds(bot_radius)

    # re-generate obstacles, start, and goal until we find a vaild path
    while True:
        try:
            # setting random-ish number and size of obstacles
            grid.obstacles = []
            for _ in range(10):
                obstacle_radius = random.uniform(0.3, 0.6)
                grid.obstacles.append(
                    Obstacle(
                        x=random.uniform(grid.min_x, grid.max_x),
                        y=random.uniform(grid.min_y, grid.max_y),
                        radius=obstacle_radius
                    )
                )

            # inflate the obstacles and bounds
            grid.inflate_obstacles(bot_radius)

            # generate start in top left of grid
            start: Node = Node(
                x=random.choice(np.arange(grid.min_x, grid.max_x // 2, grid.grid_spacing)),
                y=random.choice(np.arange(grid.max_y // 2, grid.max_y, grid.grid_spacing))
            )
            if not grid.is_valid_node(start):
                continue
        
            # generate goal in bottom right of grid
            goal: Node = Node(
                x=random.choice(np.arange(grid.max_x // 2, grid.max_x, grid.grid_spacing)),
                y=random.choice(np.arange(grid.min_y, grid.max_y // 2, grid.grid_spacing))
            )
            if not grid.is_valid_node(goal):
                continue

            # goal is minimum distance of >= some proportion of the map size
            if goal.distance(start) < Node(0, 0).distance(Node(grid.max_x, grid.max_y)) / 1.5:
                continue

            # goal is not start
            if goal == start:
                continue
            
            # find a path
            aStar: AStar = AStar(grid, start, goal, do_diagonals=True)
            aStar.find_path()
            break
        except KeyError:
            # the goal was never found, re-generate start, goal, and obstacles
            logging.info("No path found, re-generating obstacles, start, and goal")
            continue

        except ValueError:
            logging.info("No path found, re-generating obstacles, start, and goal")
            continue

    # PLOT
    fig, ax = plt.subplots()
    ax.set_title(
        f"A* ({seed})\n" \
        f"do_diagnoals={aStar.do_diagonals}, " \
        f"grid_spacing={grid.grid_spacing:.2f}m,\n" \
        f"bot_radius={bot_radius:.2f}m, " \
        f"ellapsed_time={aStar.timings['find_path'].total:.2f} sec." \
    )
    ax.set_ylabel("Y (m)")
    ax.set_xlabel("X (m)")
    
    ax.set_xlim(grid.min_x - grid.grid_spacing, grid.max_x + grid.grid_spacing)
    ax.set_ylim(grid.min_y - grid.grid_spacing, grid.max_y + grid.grid_spacing)

    # plot start and goal
    ax.plot(start.x, start.y, "o", color=Colors.green)
    ax.plot(goal.x, goal.y, "o", color=Colors.white)

    grid.plot_obstacles(ax, Colors.red)
    # aStar.plot_visited_nodes(ax, color=Colors.light_grey)

    Plot.plot_animation(fig, ax, save_animation=True)

def main() -> None:
    Logger.start_logging()
    logging.info("Started")

    # problem_2()
    problem_3()
    # for_fun()

if __name__ == "__main__":
    main()