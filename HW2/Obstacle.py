from Node import Node

class Obstacle(Node):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y)
        self.radius = radius

    ############################################################################

    def is_colliding(self, node: Node) -> bool:
        """
        Checks if an obstacle is colliding with a node
        """
        return self.distance(node) <= self.radius

    ############################################################################