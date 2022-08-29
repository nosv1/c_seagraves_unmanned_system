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
        bot_radius=0.5
    )
    nodes = [
        Node(x=2, y=2),
        Node(x=2.5, y=4.0),
        Node(x=10, y=10),
        Node(x=9.5, y=8),
    ]
    for node in nodes:
        grid.ax.text(
            node.x, 
            node.y + grid.grid_spacing / 3, 
            "Valid" if grid.node_is_valid(node) else "Invalid",
            ha="center",
            fontsize=12
        )
        grid.ax.text(
            node.x,
            node.y - grid.grid_spacing / 2,
            f"({node.x}, {node.y})",
            ha="center",
            fontsize=12
        )
        grid.ax.plot(node.x, node.y, 'ro')
    grid.plot()

if __name__ == "__main__":
    main()