import logging
import matplotlib.pyplot as plt
import numpy as np
import random
import sys

from Colors import Colors
from Dijkstra import Dijkstra
from Grid import Grid
from Logger import Logger
from Node import Node
from Obstacle import Obstacle
from Plot import Plot

def problem_1() -> None:
    obstacle_radius: float = 0.5
    obstacles = [
        Obstacle(x=1, y=1, radius=obstacle_radius),
        Obstacle(x=4, y=4, radius=obstacle_radius),
        Obstacle(x=3, y=4, radius=obstacle_radius),
        Obstacle(x=5, y=0, radius=obstacle_radius),
        Obstacle(x=5, y=1, radius=obstacle_radius),
        Obstacle(x=0, y=7, radius=obstacle_radius),
        Obstacle(x=1, y=7, radius=obstacle_radius),
        Obstacle(x=2, y=7, radius=obstacle_radius),
        Obstacle(x=3, y=7, radius=obstacle_radius),
    ]

    grid: Grid = Grid(
        min_x=0,
        max_x=10,
        min_y=0,
        max_y=10,
        grid_spacing=0.5,
        obstacles=obstacles,
    )

    check_nodes = [
        Node(2, 2),
        Node(3, 3.5),
        Node(10, 10),
        Node(10.5, 5)
    ]

    # PLOT
    fig, ax = plt.subplots()
    ax.set_title(f"Check Valid Nodes")
    ax.set_ylabel("Y")
    ax.set_xlabel("X")
    
    ax.set_xlim(grid.min_x - grid.grid_spacing, grid.max_x + grid.grid_spacing)
    ax.set_ylim(grid.min_y - grid.grid_spacing, grid.max_y + grid.grid_spacing)

    # plot obstacles
    for obstacle in grid.obstacles:
        ax.add_artist(plt.Circle(
            (obstacle.x, obstacle.y),
            obstacle.radius,
            color=Colors.red,
            fill=True
        ))
        ax.text(
            obstacle.x,
            obstacle.y,
            f"({obstacle.x:.1f}, {obstacle.y:.1f})",
            ha="center",
            va="center",
            fontsize=6
        )

    # plot check nodes
    for node in check_nodes:
        ax.plot(node.x, node.y, 'bo')
        ax.text(
            node.x,
            node.y + grid.grid_spacing / 4,
            "Valid" if grid.is_valid_node(node) else "Invalid",
            ha="center",
            fontsize=8
        )        
        ax.text(
            node.x,
            node.y - grid.grid_spacing / 2,
            f"({node.x}, {node.y})",
            ha="center",
            fontsize=8
        )

    plt.show()

def problem_2() -> None:
    start: Node = Node(x=.5, y=2)
    goal: Node = Node(x=8, y=9)

    obstacle_radius: float = 0.5
    obstacles = [
        Obstacle(x=1, y=1, radius=obstacle_radius),
        Obstacle(x=4, y=4, radius=obstacle_radius),
        Obstacle(x=3, y=4, radius=obstacle_radius),
        Obstacle(x=5, y=0, radius=obstacle_radius),
        Obstacle(x=5, y=1, radius=obstacle_radius),
        Obstacle(x=0, y=7, radius=obstacle_radius),
        Obstacle(x=1, y=7, radius=obstacle_radius),
        Obstacle(x=2, y=7, radius=obstacle_radius),
        Obstacle(x=3, y=7, radius=obstacle_radius),
    ]

    grid: Grid = Grid(
        min_x=0,
        max_x=10,
        min_y=0,
        max_y=10,
        grid_spacing=0.5,
        obstacles=obstacles,
    )
    
    dijkstra: Dijkstra = Dijkstra(grid, start, goal)
    dijkstra.find_path()

    # PLOT
    fig, ax = plt.subplots()
    ax.set_title(f"Dijkstra (no inflation)")
    ax.set_ylabel("Y")
    ax.set_xlabel("X")
    
    ax.set_xlim(grid.min_x - grid.grid_spacing, grid.max_x + grid.grid_spacing)
    ax.set_ylim(grid.min_y - grid.grid_spacing, grid.max_y + grid.grid_spacing)

    # plot start and goal
    ax.plot(start.x, start.y, "bo")
    ax.plot(goal.x, goal.y, "ro")

    # plot path
    path_x = [n.x for n in dijkstra.path]
    path_y = [n.y for n in dijkstra.path]
    ax.plot(path_x, path_y, "r-")

    grid.plot_obstacles(ax, Colors.red)
    dijkstra.plot_visited_nodes(ax, color=Colors.light_grey)

    plt.show()

def problem_3() -> None:
    start: Node = Node(x=.5, y=2)
    goal: Node = Node(x=8, y=9)
    bot_radius: float = 0.5

    obstacle_radius: float = 0.5
    obstacles = [
        Obstacle(x=1, y=1, radius=obstacle_radius),
        Obstacle(x=4, y=4, radius=obstacle_radius),
        Obstacle(x=3, y=4, radius=obstacle_radius),
        Obstacle(x=5, y=0, radius=obstacle_radius),
        Obstacle(x=5, y=1, radius=obstacle_radius),
        Obstacle(x=0, y=7, radius=obstacle_radius),
        Obstacle(x=1, y=7, radius=obstacle_radius),
        Obstacle(x=2, y=7, radius=obstacle_radius),
        Obstacle(x=3, y=7, radius=obstacle_radius),
    ]

    grid: Grid = Grid(
        min_x=0,
        max_x=10,
        min_y=0,
        max_y=10,
        grid_spacing=0.5,
        obstacles=obstacles,
    )

    grid.inflate_obstacles(bot_radius)
    grid.inflate_bounds(bot_radius)
    
    dijkstra: Dijkstra = Dijkstra(grid, start, goal)
    dijkstra.find_path()

    # PLOT
    fig, ax = plt.subplots()
    ax.set_title(f"Dijkstra (inflation)")
    ax.set_ylabel("Y")
    ax.set_xlabel("X")
    
    ax.set_xlim(grid.min_x - grid.grid_spacing, grid.max_x + grid.grid_spacing)
    ax.set_ylim(grid.min_y - grid.grid_spacing, grid.max_y + grid.grid_spacing)

    # plot start and goal
    ax.plot(start.x, start.y, "bo")
    ax.plot(goal.x, goal.y, "ro")

    # plot path
    path_x = [n.x for n in dijkstra.path]
    path_y = [n.y for n in dijkstra.path]
    ax.plot(path_x, path_y, "r-")

    grid.plot_obstacles(ax, Colors.red)
    dijkstra.plot_visited_nodes(ax, color=Colors.light_grey)

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
    # seed = 80399
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
            for _ in range(25):
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
            dijkstra: Dijkstra = Dijkstra(grid, start, goal, do_diagonals=True)
            dijkstra.find_path()
            break
        except KeyError:
            # the goal was never found, re-generate start, goal, and obstacles
            logging.info("No path found, re-generating obstacles, start, and goal")
            continue

    # PLOT
    fig, ax = plt.subplots()
    ax.set_title(
        f"Dijkstra ({seed})\n" \
        f"do_diagnoals={dijkstra.do_diagonals}, " \
        f"grid_spacing={grid.grid_spacing:.2f}m,\n" \
        f"bot_radius={bot_radius:.2f}m, " \
        f"ellapsed_time={dijkstra.timings['find_path'].total:.2f} sec." \
    )
    ax.set_ylabel("Y (m)")
    ax.set_xlabel("X (m)")
    
    ax.set_xlim(grid.min_x - grid.grid_spacing, grid.max_x + grid.grid_spacing)
    ax.set_ylim(grid.min_y - grid.grid_spacing, grid.max_y + grid.grid_spacing)

    # plot start and goal
    ax.plot(start.x, start.y, "o", color=Colors.green)
    ax.plot(goal.x, goal.y, "o", color=Colors.white)

    grid.plot_obstacles(ax, Colors.red)
    dijkstra.plot_visited_nodes(ax, color=Colors.light_grey)

    Plot.plot_animation(fig, ax, save_animation=True)

def main() -> None:
    Logger.start_logging()
    logging.info("Started")

    # problem_1()
    # problem_2()
    # problem_3()
    for_fun()

if __name__ == "__main__":
    main()