from __future__ import annotations

import json

class Node:
    def __init__(
        self, x: float, y: float, start_to_node_cost: float=0, heuristic_cost: float=0, parent: Node=None
    ):
        self.x = x
        self.y = y
        self.start_to_node_cost = start_to_node_cost
        self.heuristic_cost = heuristic_cost
        self.parent = parent

        self._id: str = self.id

    @property
    def id(self) -> str:
        return f"({self.x:.5f}, {self.y:.5f})"

    @property
    def total_cost(self) -> float:
        """
        Returns the total cost of the node
        """
        return self.start_to_node_cost + self.heuristic_cost

    ############################################################################

    def __eq__(self, other: Node) -> bool:
        """
        Checks if two nodes are equal
        """
        return self.x == other.x and self.y == other.y

    def __str__(self, to_json=False) -> str:
        """
        Returns a string representation of the node
        """
        if to_json:
            return json.dumps(self, indent=4, default=lambda o: o.__dict__)
        else:
            return f"({self.x:.5f}, {self.y:.5f})"

    ############################################################################

    def from_json(json_str: str) -> Node:
        """
        Creates a node from a json string
        """
        json_dict = json.loads(json_str)
        return Node(
            x=json_dict["_x"],
            y=json_dict["_y"],
            start_to_node_cost=json_dict["cost"]
        )

    ############################################################################

    def distance(self, other: Node) -> float:
        """
        Calculates the ecuclidean distance between two nodes
        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        
    ############################################################################