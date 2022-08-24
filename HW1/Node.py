
class Node:
    def __init__(
        self, x: float, y: float, parent_cost: float=None, index: int=None
    ):
        self.x = x
        self.y = y
        self.parent_cost = parent_cost
        self.index = index

    def distance(self, other) -> float:
        """
        Calculates the ecuclidean distance between two nodes
        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5