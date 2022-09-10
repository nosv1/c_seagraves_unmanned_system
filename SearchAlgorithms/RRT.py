import matplotlib.pyplot as plt
import numpy as np
import random

from Colors import Colors
from Node import Node
from PathFinder import PathFinder

class RRT(PathFinder):
    def __init__(self, step_length: float, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.step_length = step_length

    def generate_random_node(self) -> Node:
        self._random_node = Node(
            x=random.uniform(
                self.grid.min_x - self.grid.grid_spacing, 
                self.grid.max_x + self.grid.grid_spacing
            ),
            y=random.uniform(
                self.grid.min_y - self.grid.grid_spacing,
                self.grid.max_y + self.grid.grid_spacing
            )
        )
        return self._random_node

    def step_towards_node(self, root: Node, node: Node, step_length=None) -> Node:
        distance: float = root.distance_to(node)
        step_length: float = step_length if step_length else self.step_length
        return Node(
            x=root.x + self.step_length * (node.x - root.x) / distance,
            y=root.y + self.step_length * (node.y - root.y) / distance,
            start_to_node_cost=root.start_to_node_cost + step_length,
            parent=root
        )

    def find_closest_node(self, node: Node) -> Node:
        closest_node: Node = None
        closest_distance: float = float('inf')
        for n in self._open_set.values():
            distance: float = n.distance_to(node)
            if distance < closest_distance:
                closest_node = n
                closest_distance = distance
        return closest_node

    def is_valid_step(self, start: Node, stop: Node, resoloution: float) -> bool:
        """
        Check if points (of resolution) between start and stop are valid.
        """
        for step in np.linspace(0, 1, int(start.distance_to(stop) / resoloution)):
            node: Node = Node(
                x=start.x + step * (stop.x - start.x),
                y=start.y + step * (stop.y - start.y)
            )
            snapped_node: Node = self.grid.snap_node_to_grid(node)
            if not self.grid.node_is_valid(snapped_node):
                return False
        return True

    def find_path(self, ax: plt.Axes) -> None:
        self._open_set[self.start.id] = self.start
        while self._current_node.distance_to(self.goal) > self.step_length:
            while True:
                random_node: Node = self.grid.generate_valid_node()
                closest_node: Node = self.find_closest_node(random_node)
                self._current_node = self.step_towards_node(closest_node, random_node)
                # snapped_node: Node = self.grid.snap_node_to_grid(
                #     Node(self._current_node.x, self._current_node.y)
                # )
                if self.is_valid_step(
                    closest_node, self._current_node, self.step_length / 5
                ):
                # if self.grid.node_is_valid(snapped_node):
                    self._open_set[self._current_node.id] = self._current_node
                    # ax.plot(
                    #     random_node.x, 
                    #     random_node.y,
                    #     marker="o",
                    #     color=Colors.orange,
                    #     markersize=4
                    # )
                    # ax.plot(
                    #     closest_node.x,
                    #     closest_node.y,
                    #     marker="o",
                    #     color=Colors.light_blue,
                    #     markersize=4
                    # )
                    # ax.plot(
                    #     snapped_node.x,
                    #     snapped_node.y,
                    #     marker="o",
                    #     color=Colors.green,
                    #     markersize=4
                    # )
                    # plt.pause(0.001)
                    break

        self.goal.start_to_node_cost = (
            self._current_node.start_to_node_cost + 
            self._current_node.distance_to(self.goal)
        )
        self.goal.parent = self._current_node

        self._path = [self.goal]
        while self._path[-1].parent:
            self._path.append(self._path[-1].parent)