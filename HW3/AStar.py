import logging
import matplotlib.pyplot as plt

from Grid import Grid
from Node import Node
from Stopwatch import Stopwatch

class AStar:
    def __init__(self, grid: Grid, start: Node, goal: Node, do_diagonals=True) -> None:
        self.grid = grid
        self.start = start
        self.goal = goal
        self.do_diagonals = do_diagonals

        self._current_node: Node = start
        self._unvisited_nodes: dict[str, Node] = {
            self._current_node._id: self._current_node
        }
        self._visited_nodes: dict[str, Node] = {}
        self._path: list[Node] = []
        self._timings = {
            "find_path": Stopwatch(),
        }

    @property
    def path(self) -> list[Node]:
        return self._path

    @property
    def timings(self) -> dict[str, Stopwatch]:
        return self._timings

    ############################################################################

    def add_neighbors_to_unvisited_nodes(self):
        """
        Adds neighbors of the current node to the unvisited nodes list
        """
        logging.info(":Neighbors:Discovering neighbors...")

        # instead of nested loops, we define a list of valid moves
        diagonal_moves = [
            (-self.grid.grid_spacing, -self.grid.grid_spacing),  # left bottom
            (-self.grid.grid_spacing, self.grid.grid_spacing),   # left top
            (self.grid.grid_spacing, -self.grid.grid_spacing),   # right bottom
            (self.grid.grid_spacing, self.grid.grid_spacing),    # right top
        ]

        move_list = [
            (-self.grid.grid_spacing, 0),                        # left center
            (0, -self.grid.grid_spacing),                        # center bottom
            (0, self.grid.grid_spacing),                         # center top
            (self.grid.grid_spacing, 0),                         # right center
        ]

        if self.do_diagonals:
            move_list += diagonal_moves

        # loop through valid moves to find our neighbors
        for move in move_list:

            # define the new neighbor based on the valid move
            neighbor: Node = Node(
                x=self._current_node.x + move[0],
                y=self._current_node.y + move[1],
                parent=self._current_node
            )
            
            # check if neighbor's position is valid
            if not self.grid.is_valid_node(neighbor):
                continue

            neighbor.cost = (
                self._current_node.cost + 
                neighbor.distance(self._current_node) +
                neighbor.distance(self.goal)
            )

            # if we've noted this neighbor already as being unvisted, update cost and parent as needed
            if neighbor._id in self._unvisited_nodes:
                if neighbor.cost < self._unvisited_nodes[neighbor._id].cost:
                    self._unvisited_nodes[neighbor._id].cost = neighbor.cost
                    self._unvisited_nodes[neighbor._id].parent = self._current_node

                logging.info(f":Neighbors:Node:Visited Neighbor: {neighbor}")

            # otherwise add to unvisited
            elif neighbor._id not in self._visited_nodes:
                self._unvisited_nodes[neighbor._id] = neighbor

                logging.info(f":Neighbors:Node:Unvisted Neighbor: {neighbor}")

            else:
                logging.info(f":Neighbors:Node:Visited Neighbor: {neighbor}")

    def find_path(self) -> list[Node]:
        """
        Finds the shortest path between two nodes using Dijkstra's algorithm
        :param: start: start node
        :param: end: end node
        :param: grid: grid to search on
        :return: list of nodes in the shortest path
        """
        logging.info("Visiting all Nodes...")
        self._timings["find_path"].start()

        # while there exists unvisted nodes
        while self._current_node != self.goal:
            # visit current node
            self._visited_nodes[self._current_node._id] = self._current_node

            # get lowest cost unvisited node
            self._current_node = min(self._unvisited_nodes.values(), key=lambda x: x.cost)
            logging.info(f":Node:Current Node: Node({self._current_node.x}, {self._current_node.y}, {self._current_node.cost})")

            # remove old node from unvisited nodes
            del self._unvisited_nodes[self._current_node._id]

            # add neighbors of current node to unvisited nodes, updating costs and parent as necessary
            self.add_neighbors_to_unvisited_nodes()
        self._visited_nodes[self._current_node._id] = self._current_node

        self._timings["find_path"].stop()
        logging.info(f"Visited all Nodes in {self._timings['find_path'].total:.3f} seconds")
        logging.info("All Nodes visited...")

        # backtrack to find path starting at the goal node
        self._path = [
            self._visited_nodes[self.goal._id]
        ]
        while self._path[-1].parent:
            self._path.append(self._visited_nodes[self._path[-1].parent._id])

        logging.info("Path found...")
        logging.info(f":Path: {', '.join([str(node) for node in self._path])}")
            
    ############################################################################

    def plot_visited_nodes(self, ax: plt.Axes, color: str) -> None:
        """
        Plots the visited nodes
        :param: ax: matplotlib axes to plot on
        :param: color: color to plot the nodes
        """
        for node in self._visited_nodes.values():
            ax.text(
                node.x, 
                node.y, 
                f"{node.cost:.1f}", 
                ha="center", 
                va="center",
                fontsize=6,
                color=color
            )
            
    ############################################################################