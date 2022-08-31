from Grid import Grid
from Node import Node

class Dijkstra:
    def __init__(self, grid: Grid, start: Node, goal: Node) -> None:
        self.start = start
        self.goal = goal
        self.grid = grid

        self.current_node: Node = start
        self.unvisited_nodes: dict[int, Node] = {
            self.current_node._id: self.current_node
        }
        self.visited_nodes: dict[int, Node] = {}
        self.path: list[Node] = []

    def add_neighbors_to_unvisited_nodes(self):
        """
        Adds neighbors of the current node to the unvisited nodes list
        """
        # instead of nested loops, we define a list of valid moves 
        move_list = [
            (-self.grid.grid_spacing, -self.grid.grid_spacing),  # left bottom
            (-self.grid.grid_spacing, 0),                        # left center
            (-self.grid.grid_spacing, self.grid.grid_spacing),   # left top
            (0, -self.grid.grid_spacing),                        # center bottom
            (0, self.grid.grid_spacing),                         # center top
            (self.grid.grid_spacing, -self.grid.grid_spacing),   # right bottom
            (self.grid.grid_spacing, 0),                         # right center
            (self.grid.grid_spacing, self.grid.grid_spacing),    # right top
        ]

        # loop through valid moves to find our neighbors
        for move in move_list:

            # define the new neighbor based on the valid move
            neighbor: Node = Node(
                x=self.current_node._x + move[0],
                y=self.current_node._y + move[1],
                parent=self.current_node
            )
            
            # check if neighbor's position is valid
            if not self.grid.node_is_valid(neighbor):
                continue

            neighbor.cost = self.current_node.cost + neighbor.distance(self.current_node)

            # if we've noted this neighbor already as been unvisted, update cost and parent as needed
            if neighbor._id in self.unvisited_nodes:
                if neighbor.cost < self.unvisited_nodes[neighbor._id].cost:
                    self.unvisited_nodes[neighbor._id].cost = neighbor.cost
                    self.unvisited_nodes[neighbor._id].parent = self.current_node

            # otherwise add to unvisited
            elif neighbor._id not in self.visited_nodes:
                self.unvisited_nodes[neighbor._id] = neighbor

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
            self.visited_nodes[self.current_node._id] = self.current_node

            # get lowest cost unvisited node
            self.current_node = min(self.unvisited_nodes.values(), key=lambda x: x.cost)

            # remove old node from unvisited nodes
            del self.unvisited_nodes[self.current_node._id]

            # add neighbors of current node to unvisited nodes, updating costs and parent as necessary
            self.add_neighbors_to_unvisited_nodes()
        self.visited_nodes[self.current_node._id] = self.current_node

        # backtrack to find path starting at the goal node
        self.path = [
            self.visited_nodes[self.goal._id]
        ]
        while self.path[-1].parent:
            self.path.append(self.visited_nodes[self.path[-1].parent._id])