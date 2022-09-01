from datetime import datetime
import logging
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from Dijkstra import Dijkstra
from Grid import Grid
from Node import Node
from Obstacle import Obstacle

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
            color="red",
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
            color="red",
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
            color="red",
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

def plot_animation(fig, ax):
    log_filename: str = logging.getLogger().handlers[0].baseFilename
    logging.info("Finished")
    logging.shutdown()

    with open(log_filename, "r") as f:
        lines = f.readlines()

    light_blue = "#ADD8E6"
    dark_grey = "#A9A9A9"
    green = "#008000"
    dark_red = "#8B0000"

    path_line, = ax.plot([], [], "-", color=light_blue)
    unvisted_neighbors_plot, = ax.plot([], [], "o", color=green)
    visited_neighbors_plot, = ax.plot([], [], "o", color=dark_grey)
    invalid_neighbors_plot, = ax.plot([], [], "o", color=dark_red)

    neighbor_frames = []
    path_frames = []

    unvisted_neighbors: list[tuple] = []
    visited_neighbors: list[tuple] = []
    invalid_neighbors: list[tuple] = []
    
    for line in lines:
        if ":Path:" in line:
            path_frames = eval(f"[{line.split(':Path:')[1]}]")[::-1]

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
            return unvisted_neighbors_plot, visited_neighbors_plot, invalid_neighbors_plot

        else:
            path_line.set_data(
                [n[0] for n in path_frames[:i-len(neighbor_frames)]],
                [n[1] for n in path_frames[:i-len(neighbor_frames)]]
            )
            return path_line,

    animation = FuncAnimation(
        fig, 
        update, 
        frames=len(neighbor_frames) + len(path_frames) + 30, 
        repeat=False, 
        interval=20, blit=True
    )
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
    grid: Grid = Grid(
        min_x=0,
        max_x=10,
        min_y=0,
        max_y=10,
        grid_spacing=0.5,
        obstacles=[
            Obstacle(x=1, y=1, radius=obstacle_radius),
            Obstacle(x=4, y=4, radius=obstacle_radius),
            Obstacle(x=3, y=4, radius=obstacle_radius),
            Obstacle(x=5, y=0, radius=obstacle_radius),
            Obstacle(x=5, y=1, radius=obstacle_radius),
            Obstacle(x=0, y=7, radius=obstacle_radius),
            Obstacle(x=1, y=7, radius=obstacle_radius),
            Obstacle(x=2, y=7, radius=obstacle_radius),
            Obstacle(x=3, y=7, radius=obstacle_radius),
        ],
    )
    
    ax.set_xlim(grid.min_x - grid.grid_spacing, grid.max_x + grid.grid_spacing)
    ax.set_ylim(grid.min_y - grid.grid_spacing, grid.max_y + grid.grid_spacing)

    # problem_1(ax, grid)
    # problem_2(ax, grid)
    problem_3(ax, grid)

    plot_animation(fig, ax)

if __name__ == "__main__":
    main()