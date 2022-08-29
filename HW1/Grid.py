import matplotlib.pyplot as plt

from Node import Node

################################################################################

class Grid:
    def __init__(self, max_x: int, max_y: int, grid_spacing: float) -> None:
        self.max_x = max_x
        self.max_y = max_y
        self.grid_spacing = grid_spacing
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
    # PLOT

    def plot_nodes(self) -> None:
        """
        Plots the nodes in the grid
        """
        for node in self.nodes:
            self.ax.text(node.x, node.y, node.index, color="red", fontsize="8")

    def plot(self):
        self.ax.set_title(f"Node Grid\nGrid Spacing: {self.grid_spacing}")
        self.ax.set_ylabel("Y")
        self.ax.set_xlabel("X")
        self.ax.set_xlim(0, self.max_x + self.grid_spacing)
        self.ax.set_ylim(0, self.max_y + self.grid_spacing)
        
        self.plot_nodes()
        plt.show()
        plt.close()

    ############################################################################