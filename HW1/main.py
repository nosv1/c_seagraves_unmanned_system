from Grid import Grid
from Node import Node

def main():
    grid: Grid = Grid(
        max_x=10,
        max_y=10,
        grid_spacing=0.5,
        obstacles=[
            Node(x=1, y=1),
            Node(x=4, y=4),
            Node(x=3, y=4),
            Node(x=5, y=0),
            Node(x=5, y=1),
            Node(x=0, y=7),
            Node(x=1, y=7),
            Node(x=2, y=7),
            Node(x=3, y=7)
        ],
        obstacle_radius=0.5
    )
    nodes = [
        Node(x=2, y=2),
        Node(x=2.9, y=3.6),
    ]
    for node in nodes:
        grid.ax.text(
            node.x, 
            node.y + grid.grid_spacing / 4, 
            "Invalid" if grid.node_in_obstacle(node) else "Valid",
            ha="center"
        )
        grid.ax.plot(node.x, node.y, 'ro')
    grid.plot()

if __name__ == "__main__":
    main()