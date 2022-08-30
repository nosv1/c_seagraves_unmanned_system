from Node import Node

class Obstacle:
    def __init__(self, node: Node, radius: float) -> None:
        self.node = node
        self.radius = radius

    def is_colliding(self, node: Node) -> bool:
        """
        Checks if an obstacle is colliding with a node
        """
        return self.node.distance(node) <= self.radius