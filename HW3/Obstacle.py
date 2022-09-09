from Node import Node

class Obstacle(Node):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y)
        self.radius = radius
        self.bounding_box = self.get_bounding_box()

    ############################################################################

    def get_bounding_box(self, do_diagonal=True) -> set[Node]:
        """
        Returns the bounding box of the obstacle
        """

    def is_colliding(self, node: Node) -> bool:
        """
        Checks if an obstacle is colliding with a node
        """
        return self.distance(node) < self.radius

    ############################################################################