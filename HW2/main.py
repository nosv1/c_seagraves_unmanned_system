from dataclasses import dataclass
from datetime import datetime
import logging
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

from Dijkstra import Dijkstra
from Grid import Grid
from Node import Node
from Obstacle import Obstacle

@dataclass
class Colors:
    black = "#000000"
    dark_green = "#008000"
    dark_grey = "#A9A9A9"
    dark_red = "#A1323B"
    green = "#98C379"
    grey = "#282C34"
    light_grey = "#ABB2BF"
    light_blue = "#61AFEF"
    red = "#E06C75"
    white = "#FFFFFF"
    
def setup_logging():
    logging.basicConfig(
        filename=f"HW2/Logs/{datetime.now().strftime('%Y-%m-%d %H-%M-%S')}.log", 
        level=logging.INFO
    )
    logging.info("Started")

def problem_1(ax, grid: Grid):
    check_nodes = [
        Node(2, 2),
        Node(3, 3.5),
        Node(10, 10),
        Node(10.5, 5)
    ]

    ############################################################################
    # PLOT

    ax.set_title(f"Check Valid Nodes")

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
        ax.plot(node._x, node._y, 'bo')
        ax.text(
            node._x,
            node._y + grid.grid_spacing / 4,
            "Valid" if grid.node_is_valid(node) else "Invalid",
            ha="center",
            fontsize=8
        )        
        ax.text(
            node._x,
            node._y - grid.grid_spacing / 2,
            f"({node._x}, {node._y})",
            ha="center",
            fontsize=8
        )

    return ax

def problem_2(ax, grid):
    start: Node = Node(x=.5, y=2)
    goal: Node = Node(x=8, y=9)
    
    dijkstra: Dijkstra = Dijkstra(grid, start, goal)
    dijkstra.find_path()

    ############################################################################
    # PLOT

    ax.set_title(f"Dijkstra (no inflation)")

    # plot start and goal
    ax.plot(start._x, start._y, "bo")
    ax.plot(goal._x, goal._y, "ro")

    # plot path
    path_x = [n._x for n in dijkstra.path]
    path_y = [n._y for n in dijkstra.path]
    ax.plot(path_x, path_y, "r-")

    # plot obstacles
    for obstacle in grid.obstacles:
        ax.add_artist(plt.Circle(
            (obstacle.x, obstacle.y),
            obstacle.radius,
            color=Colors.red,
            fill=True
        ))

    # plot dijkstra visited nodes
    for node in dijkstra.visited_nodes.values():
        ax.text(
            node._x, 
            node._y, 
            f"{node.cost:.1f}", 
            ha="center", 
            va="center",
            fontsize=6
        )

    return ax

def problem_3(ax, grid: Grid):
    start: Node = Node(x=.5, y=2)
    goal: Node = Node(x=8, y=9)
    bot_radius: float = 0.5

    grid.inflate_obstacles(bot_radius)
    grid.shrink_bounds(bot_radius)
    
    dijkstra: Dijkstra = Dijkstra(grid, start, goal)
    dijkstra.find_path()

    ############################################################################
    # PLOT

    ax.set_title(f"Dijkstra (inflation)")

    # plot start and goal
    ax.plot(start._x, start._y, "bo")
    ax.plot(goal._x, goal._y, "ro")

    # plot path
    # path_x = [n._x for n in dijkstra.path]
    # path_y = [n._y for n in dijkstra.path]
    # ax.plot(path_x, path_y, "r-")

    # plot obstacles
    for obstacle in grid.obstacles:
        ax.add_artist(plt.Circle(
            (obstacle._x, obstacle._y),
            obstacle.radius,
            color=Colors.red,
            fill=True
        ))

    # plot dijkstra visited nodes
    for node in dijkstra.visited_nodes.values():
        ax.text(
            node._x, 
            node._y, 
            f"{node.cost:.1f}", 
            ha="center", 
            va="center",
            fontsize=6
        )

    return ax

def for_fun(ax, grid: Grid):
    bot_radius: float = 0.5

    obstacles: list[Obstacle] = []

    for _ in range(random.randrange(20, 30)):
        obstacle_radius = random.uniform(0.2, 0.5)
        obstacles.append(
            Obstacle(
                x=random.uniform(0, 10),
                y=random.uniform(0, 10),
                radius=obstacle_radius
            )
        )

    grid.obstacles = obstacles

    grid.inflate_obstacles(bot_radius)
    grid.shrink_bounds(bot_radius)
    grid.valid_nodes = grid.get_valid_nodes()

    start = random.choice(grid.valid_nodes)
    while True:
        goal = random.choice(grid.valid_nodes)
        if goal.distance(start) < Node(0, 0).distance(Node(grid.max_x, grid.max_y)) / 2:
            continue
        if goal != start:
            break
    
    dijkstra: Dijkstra = Dijkstra(grid, start, goal)
    dijkstra.find_path()

    ############################################################################
    # PLOT

    ax.set_title(f"Dijkstra (inflation)")

    # plot start and goal
    ax.plot(start._x, start._y, "o", color=Colors.green)
    ax.plot(goal._x, goal._y, "o", color=Colors.white)

    # plot obstacles
    for obstacle in grid.obstacles:
        ax.add_artist(plt.Circle(
            (obstacle._x, obstacle._y),
            obstacle.radius,
            color=Colors.red,
            fill=True
        ))

    # plot dijkstra visited nodes
    for node in dijkstra.visited_nodes.values():
        ax.text(
            node._x, 
            node._y, 
            f"{node.cost:.1f}", 
            ha="center", 
            va="center",
            fontsize=6,
            color=Colors.light_grey
        )

    return ax

def plot_animation(fig, ax):
    log_filename: str = logging.getLogger().handlers[0].baseFilename
    logging.info("Finished")
    logging.shutdown()

    with open(log_filename, "r") as f:
        lines = f.readlines()

    path_line, = ax.plot([], [], "-", color=Colors.light_blue, linewidth=3)
    unvisted_neighbors_plot, = ax.plot([], [], "o", color=Colors.dark_green)
    visited_neighbors_plot, = ax.plot([], [], "o", color=Colors.dark_grey)
    invalid_neighbors_plot, = ax.plot([], [], "o", color=Colors.dark_red)

    neighbor_frames = []
    path_frames = []

    unvisted_neighbors: list[tuple] = []
    visited_neighbors: list[tuple] = []
    invalid_neighbors: list[tuple] = []

    path_frames_per_frame = 3
    
    for line in lines:
        if ":Path:" in line:
            path_frames: list[tuple] = eval(f"[{line.split(':Path:')[1]}]")[::-1]
            i = len(path_frames) - 1
            while i >= 0:
                for j in range(path_frames_per_frame - 1):
                    path_frames.insert(i + 1, path_frames[i])
                i -= 1

        elif ":Neighbors:" in line:
            if ":Discovering neighbors..." in line:
                neighbor_frames.append(
                    {
                        "unvisted_neighbors": unvisted_neighbors.copy(),
                        "visited_neighbors": visited_neighbors.copy(),
                        "invalid_neighbors": invalid_neighbors.copy()
                    }
                )
                unvisted_neighbors = []
                visited_neighbors = []
                invalid_neighbors = []

            elif ":Visited Neighbor:" in line:
                visited_neighbors.append(eval(line.split(":Visited Neighbor:")[1]))

            elif ":Unvisted Neighbor:" in line:
                unvisted_neighbors.append(eval(line.split(":Unvisted Neighbor:")[1]))

        elif ":Node:" in line:
            if ":In obstacle:" in line:
                invalid_neighbors.append(eval(line.split(":In obstacle:")[1]))
            elif ":Out of bounds:" in line:
                invalid_neighbors.append(eval(line.split(":Out of bounds:")[1]))

    frames = neighbor_frames + path_frames

    def update(i):
        if i < len(neighbor_frames):
            unvisted_neighbors_plot.set_data(
                [n[0] for n in neighbor_frames[i]["unvisted_neighbors"]],
                [n[1] for n in neighbor_frames[i]["unvisted_neighbors"]]
            )
            visited_neighbors_plot.set_data(
                [n[0] for n in neighbor_frames[i]["visited_neighbors"]],
                [n[1] for n in neighbor_frames[i]["visited_neighbors"]]
            )
            invalid_neighbors_plot.set_data(
                [n[0] for n in neighbor_frames[i]["invalid_neighbors"]],
                [n[1] for n in neighbor_frames[i]["invalid_neighbors"]]
            )
            path_line.set_data([], [])

        else:
            unvisted_neighbors_plot.set_data([], [])
            visited_neighbors_plot.set_data([], [])
            invalid_neighbors_plot.set_data([], [])
            path_line.set_data(
                [n[0] for n in path_frames[:i-len(neighbor_frames)]],
                [n[1] for n in path_frames[:i-len(neighbor_frames)]]
            )

        return unvisted_neighbors_plot, visited_neighbors_plot, invalid_neighbors_plot, path_line,

    fig.patch.set_facecolor(Colors.grey)
    ax.set_facecolor(Colors.grey)
    ax.title.set_color(Colors.light_grey)
    ax.xaxis.label.set_color(Colors.light_grey)
    ax.yaxis.label.set_color(Colors.light_grey)
    ax.tick_params(axis='x', colors=Colors.light_grey)
    ax.tick_params(axis='y', colors=Colors.light_grey)

    legend_elements = [
        Line2D([0], [0], marker='o', color=Colors.red, label='Obstacles', markerfacecolor=Colors.red, markersize=10),
        Line2D([0], [0], marker='o', color=Colors.green, label='Start', markerfacecolor=Colors.green, markersize=10),
        Line2D([0], [0], marker='o', color=Colors.white, label='Goal', markerfacecolor=Colors.white, markersize=10),
        Line2D([0], [0], color=Colors.light_blue, lw=4, label='Path'),
        Line2D([0], [0], marker='o', color=Colors.dark_green, label='Unvisted Neighbors', markerfacecolor=Colors.dark_green, markersize=10),
        Line2D([0], [0], marker='o', color=Colors.dark_grey, label='Visited Neighbors', markerfacecolor=Colors.dark_grey, markersize=10),
        Line2D([0], [0], marker='o', color=Colors.dark_red, label='Invalid Neighbors', markerfacecolor=Colors.dark_red, markersize=10),
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    animation = FuncAnimation(
        fig, 
        update, 
        frames=len(frames) + 30,
        repeat=True, 
        interval=30, blit=True
    )

    plt.show()

    animation.save(
        "animation.gif", 
        writer="Pillow", 
        fps=30, 
        progress_callback=lambda i, n: print(f"Saving frame {i} of {n}")
    )

def main():
    setup_logging()

    fig, ax = plt.subplots()
    ax.set_ylabel("Y")
    ax.set_xlabel("X")

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
    
    ax.set_xlim(grid.min_x - grid.grid_spacing, grid.max_x + grid.grid_spacing)
    ax.set_ylim(grid.min_y - grid.grid_spacing, grid.max_y + grid.grid_spacing)

    # problem_1(ax, grid)
    # problem_2(ax, grid)
    # problem_3(ax, grid)
    for_fun(ax, grid)

    plot_animation(fig, ax)

if __name__ == "__main__":
    main()