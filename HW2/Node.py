class Node:
    def __init__(
        self, x: float, y: float, cost: float=0, parent_index: int=None
    ):
        self.x = x
        self.y = y
        self.cost = cost
        self.parent_index = parent_index
        self.index: int = None

    def __eq__(self, other) -> bool:
        """
        Checks if two nodes are equal
        """
        return self.x == other.x and self.y == other.y

    ############################################################################

    def distance(self, other) -> float:
        """
        Calculates the ecuclidean distance between two nodes
        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        
    ############################################################################