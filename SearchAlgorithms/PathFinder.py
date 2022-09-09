import matplotlib.pyplot as plt

from Grid import Grid
from Node import Node
from Stopwatch import Stopwatch

class PathFinder:
    def __init__(
        self, 
        start: Node, 
        goal: Node, 
        grid: Grid, 
        do_diagonals: bool = True
    ) -> None:
        self.start = start
        self.goal = goal
        self.grid = grid
        self.do_diagonals = do_diagonals

        self._current_node: Node = self.start
        self._open_set: dict[str, Node] = {}
        self._closed_set: dict[str, Node] = {}
        self._path: list[Node] = []

        self.stopwatch: Stopwatch = Stopwatch()

    def plot_path(self, ax: plt.Axes, color: str) -> None:
        """
        Plots the path on the given axes
        """
        ax.plot(
            [node.x for node in self._path],
            [node.y for node in self._path],
            color=color,
            linewidth=3
        )

    def plot_open_set(self, ax: plt.Axes, color: str) -> None:
        """
        Plots the open set on the given axes
        """
        for node in self._open_set.values():
            ax.text(
                node.x, node.y, f"{node.total_cost:.1f}", 
                color=color, ha="center", va="center",
                fontsize=6
            )

    def plot_closed_set(self, ax: plt.Axes, color: str) -> None:
        """
        Plots the closed set on the given axes
        """
        for node in self._closed_set.values():
            ax.text(
                node.x, node.y, f"{node.total_cost:.1f}", 
                color=color, ha="center", va="center",
                fontsize=6
            )