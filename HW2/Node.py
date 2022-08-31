from __future__ import annotations

class Node:
    def __init__(
        self, x: float, y: float, cost: float=0, parent: Node=None
    ):
        self._x = x
        self._y = y
        self.cost = cost
        self.parent = parent
        self._id: str = f"({self._x:.1f}, {self._y:.1f})"

    def __eq__(self, other: Node) -> bool:
        """
        Checks if two nodes are equal
        """
        return self._x == other.x and self._y == other.y

    ############################################################################

    def distance(self, other: Node) -> float:
        """
        Calculates the ecuclidean distance between two nodes
        """
        return ((self._x - other._x) ** 2 + (self._y - other._y) ** 2) ** 0.5
        
    ############################################################################