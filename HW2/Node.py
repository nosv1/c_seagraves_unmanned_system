from __future__ import annotations

import json

class Node:
    def __init__(
        self, x: float, y: float, cost: float=0, parent: Node=None
    ):
        self._x = x
        self._y = y
        self._id: str = f"({self._x:.5f}, {self._y:.5f})"
        self.cost = cost
        self.parent = parent

    def __eq__(self, other: Node) -> bool:
        """
        Checks if two nodes are equal
        """
        return self._x == other._x and self._y == other._y

    def __str__(self, to_json=False) -> str:
        """
        Returns a string representation of the node
        """
        if to_json:
            return json.dumps(self, indent=4, default=lambda o: o.__dict__)
        else:
            return f"({self._x:.5f}, {self._y:.5f})"

    def from_json(json_str: str) -> Node:
        """
        Creates a node from a json string
        """
        json_dict = json.loads(json_str)
        return Node(
            x=json_dict["_x"],
            y=json_dict["_y"],
            cost=json_dict["cost"]
        )

    ############################################################################

    def distance(self, other: Node) -> float:
        """
        Calculates the ecuclidean distance between two nodes
        """
        return ((self._x - other._x) ** 2 + (self._y - other._y) ** 2) ** 0.5
        
    ############################################################################