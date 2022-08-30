import matplotlib.pyplot as plt

from Dijkstra import Dijkstra
from Grid import Grid
from Node import Node
from Obstacle import Obstacle

def main():
    obstacle_radius: float = 0.5
    grid: Grid = Grid(
        max_x=10,
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
    start: Node = Node(x=0, y=0, parent_index=-1)
    goal: Node = Node(x=8, y=9)
    
    dijkstra: Dijkstra = Dijkstra(grid, start, goal)
    dijkstra.find_path()

    ############################################################################
    # PLOT

    fig, ax = plt.subplots()

    ax.set_title(f"Dijkstra (no inflation)")
    ax.set_ylabel("Y")
    ax.set_xlabel("X")
    ax.set_xlim(0 - grid.grid_spacing, grid.max_x + grid.grid_spacing)
    ax.set_ylim(0 - grid.grid_spacing, grid.max_y + grid.grid_spacing)

    # plot start and goal
    ax.plot(start.x, start.y, "bo")
    ax.plot(goal.x, goal.y, "ro")

    # plot path
    path_x = [n.x for n in dijkstra.path]
    path_y = [n.y for n in dijkstra.path]
    ax.plot(path_x, path_y, "r-")

    # plot obstacles
    for obstacle in grid.obstacles:
        ax.add_artist(plt.Circle(
            (obstacle.x, obstacle.y),
            obstacle.radius,
            color="red",
            fill=False
        ))

    # plot dijkstra visited nodes
    for node in dijkstra.visited_nodes.values():
        ax.text(
            node.x, node.y, f"{node.cost:.1f}", ha="center", va="center",
        )
    
    plt.show()

if __name__ == "__main__":
    main()