from __future__ import annotations
import matplotlib.pyplot as plt

from Colors import Colors
from Grid import Grid
from Node import Node

class Path:
    def __init__(self, start: Node, goal: Node, grid: Grid) -> None:
        self.start = start
        self.goal = goal
        self.grid = grid

        self._current_node: Node = self.start
        self._open_set: dict[str, Node] = {
            self.start.id: self.start
        }
        self._closed_set: dict[str, Node] = {}
        self._path = []

    @property
    def path(self) -> list[Node]:
        return self._path

    def plot_path(self, ax: plt.Axes, color: str = Colors.light_blue) -> None:
        ax.plot(
            [n.x for n in self._path],
            [n.y for n in self._path],
            color=color,
            linewidth=2,
            marker='o',
        )