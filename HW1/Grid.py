import matplotlib.pyplot as plt

from Node import Node

################################################################################

class Grid:
    def __init__(self, 
        max_x: int, 
        max_y: int, 
        grid_spacing: float, 
        obstacles: list[Node], 
        bot_radius: float
    ) -> None:
        self.max_x = max_x
        self.max_y = max_y
        self.grid_spacing = grid_spacing
        self.obstacles = obstacles
        self.bot_radius = bot_radius
        self.nodes = self.get_nodes()

        self.fig, self.ax = plt.subplots()
        
    ############################################################################

    def get_nodes(self) -> list[Node]:
        """
        Creates a list of nodes in the grid
        """
        nodes = []
        for row in range(int(self.max_x / self.grid_spacing + 1)):
            for col in range(int(self.max_y / self.grid_spacing + 1)):
                node = Node(
                    x=col * self.grid_spacing,
                    y=row * self.grid_spacing,
                )
                node.index = self.calculate_node_index(node.x, node.y)
                nodes.append(node)
        return nodes

    def calculate_node_index(self, x: float, y: float) -> int:
        """
        Calculates the index of a node in the grid
        :param x: x-coordinate of the node
        :param y: y-coordinate of the node
        :return: index of the node
        """
        # index = row_len * y + x
        return int(
            ((self.max_x / self.grid_spacing) + 1) *  # row len * 
            (y / self.grid_spacing) +                 # y +
            (x / self.grid_spacing)                   # x
        )

    ############################################################################
    # NODE VALIDITY

    def node_in_obstacle(self, position: Node) -> bool:
        """
        Checks if a position is in an obstacle
        :param position: position to check
        :return: True if in obstacle, False otherwise
        """
        for obstacle in self.obstacles:
            if position.distance(obstacle) <= self.bot_radius:
                return True
        return False
        
    def node_in_bounds(self, position: Node) -> bool:
        """
        Checks if a position is in the bounds of the grid
        :param position: position to check
        :return: True if in bounds, False otherwise
        """
        return (
            0 + self.bot_radius <= position.x <= self.max_x - self.bot_radius and
            0 + self.bot_radius <= position.y <= self.max_y - self.bot_radius
        )

    def node_is_valid(self, position: Node) -> bool:
        """
        Checks if a position is valid
        :param position: position to check
        :return: True if valid, False otherwise
        """
        return (
            self.node_in_bounds(position) and 
            not self.node_in_obstacle(position)
        )        

    ############################################################################
    # PLOT

    def plot_nodes(self) -> None:
        """
        Plots the nodes in the grid
        """
        for node in self.nodes:
            self.ax.text(node.x, node.y, node.index, color="red", fontsize="8")

    def plot_obstacles(self) -> None:
        """
        Plots the obstacles in the grid
        """
        for obstacle in self.obstacles:
            self.ax.text(
                obstacle.x,
                obstacle.y,
                f"({obstacle.x}, {obstacle.y})",
                ha="center",
                va="center",
                fontsize=12
            )
            self.ax.add_artist(plt.Circle(
                (obstacle.x, obstacle.y),
                self.bot_radius,
                color="red",
                fill=False
            ))

    def plot(self):
        self.ax.set_title(
            f"Valid Positions (obstacles)\n" \
            f"Grid Spacing: {self.grid_spacing}, Obstacle Radius: {self.bot_radius}"
        )
        self.ax.set_ylabel("Y")
        self.ax.set_xlabel("X")
        self.ax.set_xlim(0, self.max_x + self.grid_spacing)
        self.ax.set_ylim(0, self.max_y + self.grid_spacing)
        
        # self.plot_nodes()
        self.plot_obstacles()
        plt.show()
        plt.close()

    ############################################################################