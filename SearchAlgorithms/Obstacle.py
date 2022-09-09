from __future__ import annotations
import numpy as np

from Node import Node

class Obstacle(Node):
    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y)
        self.radius = radius

        self._bounding_box: dict[str, Node] = {}

    def obstacles_from_file(
        filename: str, radius: float, delimter: str=","
    ) -> dict[str, Obstacle]:
        obstacles: dict[str, Obstacle] = {}
        with open(filename) as f:
            for line in f:
                x, y = line.split(delimter)
                obstacle: Obstacle = Obstacle(
                    x=float(x), y=float(y), radius=radius
                )
                obstacles[obstacle.id] = obstacle
        return obstacles

    def inflate(self, inflation_amount):
        """
        Inflates the obstacle

        :param inflation_amount: amount to inflate the obstacle by
        :return: None
        """
        self.radius += inflation_amount

    def set_bounding_box(self, spacing: float, include_diaganols=True) -> None:
        """
        The nodes surrounding the obstacle are its bounding box

        :param spacing: spacing
        :return: None
        """
        for x in np.arange(
            self.x - self.radius, self.x + self.radius + spacing, spacing
        ):
            for y in np.arange(
                self.y - self.radius, self.y + self.radius + spacing, spacing
            ):
                node: Node = Node(x, y, parent=self)
                if self.is_point_inside_obstacle(node):
                    self._bounding_box[node.id] = node

    def is_point_inside_obstacle(self, node: Node) -> bool:
        """
        Checks if a point is inside the obstacle

        :param node: node to check
        :return: True if the point is inside the obstacle, False otherwise
        """
        return self.distance_to(node) <= self.radius