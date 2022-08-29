import numpy as np

from Grid import Grid
from Node import Node

class Dijkstra:
    def __init__(self, grid: Grid, start: Node, goal: Node) -> None:
        self.start = start
        self.goal = goal
        self.grid = grid

        self.current_node: Node = start
        self.current_node.index = self.grid.calculate_node_index(self.current_node.x, self.current_node.y)
        self.unvisited_nodes: dict[int, Node] = {
            self.current_node.index: self.current_node
        }
        self.visited_nodes: dict[int, Node] = {}
        self.path: list[Node] = []

    def add_neighbors_to_unvisited_nodes(self):
        """
        Adds neighbors of the current node to the unvisited nodes list
        """
        for x in np.arange(
            self.current_node.x - self.grid.grid_spacing, 
            self.current_node.x + self.grid.grid_spacing * 2,
            self.grid.grid_spacing
        ):
            for y in np.arange(
                self.current_node.y - self.grid.grid_spacing, 
                self.current_node.y + self.grid.grid_spacing * 2,
                self.grid.grid_spacing
            ):
                neighbor: Node = Node(x=x, y=y)
                neighbor.index = self.grid.calculate_node_index(neighbor.x, neighbor.y)

                if self.current_node == neighbor:
                    continue
                if not self.grid.node_is_valid(neighbor):
                    continue

                neighbor.cost = self.current_node.cost + neighbor.distance(self.current_node)

                if neighbor.index in self.unvisited_nodes:
                    if neighbor.cost < self.unvisited_nodes[neighbor.index].cost:
                        self.unvisited_nodes[neighbor.index].cost = neighbor.cost
                        self.unvisited_nodes[neighbor.index].parent_index = self.current_node.index

                elif neighbor.index not in self.visited_nodes:
                    self.unvisited_nodes[neighbor.index] = neighbor
                    self.unvisited_nodes[neighbor.index].parent_index = self.current_node.index

    def find_path(self) -> list[Node]:
        """
        Finds the shortest path between two nodes using Dijkstra's algorithm
        :param: start: start node
        :param: end: end node
        :param: grid: grid to search on
        :return: list of nodes in the shortest path
        """
        while self.unvisited_nodes.keys():
            # visit current node
            self.visited_nodes[self.current_node.index] = self.current_node

            # get lowest cost unvisited node
            self.current_node = min(self.unvisited_nodes.values(), key=lambda x: x.cost)
            self.current_node.index = self.grid.calculate_node_index(self.current_node.x, self.current_node.y)

            # remove old node from unvisited nodes
            del self.unvisited_nodes[self.current_node.index]

            # add neighbors of current node to unvisited nodes, updating costs and parent as necessary
            self.add_neighbors_to_unvisited_nodes()
        self.visited_nodes[self.current_node.index] = self.current_node

        # backtrack to find path starting at the goal node
        self.path = self.visited_nodes[
            self.grid.calculate_node_index(self.goal.x, self.goal.y)
        ]
        self.path = [self.visited_nodes[self.grid.calculate_node_index(self.goal.x, self.goal.y)]]
        while self.path[-1].parent_index != -1:
            self.path.append(self.visited_nodes[self.path[-1].parent_index])