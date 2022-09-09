from __future__ import annotations
import json
import matplotlib.pyplot as plt

from AStar import AStar
from RRT import RRT
from Grid import Grid
from Node import Node
from Obstacle import Obstacle

class Scenario:
    def loader(self, filename) -> Scenario:
        with open(filename) as f:
            data = json.load(f)

        self.bot_radius = float(data["bot_radius"])
        self.start: Node = Node(
            x=float(data["start"][0]), y=float(data["start"][1])
        )
        self.goal: Node = Node(
            x=float(data["goal"][0]), y=float(data["goal"][1])
        )

        self.obstacle_radius = data["obstacle_radius"]
        self.obstacles = Obstacle.obstacles_from_file(
            data["obstacles"], self.obstacle_radius
        )

        self.grid: Grid = Grid(
            min_x=float(data["x_bounds"][0]),
            max_x=float(data["x_bounds"][1]),
            min_y=float(data["y_bounds"][0]),
            max_y=float(data["y_bounds"][1]),
            grid_spacing=float(data["grid_spacing"]),
            obstacles=self.obstacles
        )

        self.algorithm: RRT | AStar = eval(data["algorithm"]["type"])(
            start=self.start,
            goal=self.goal,
            grid=self.grid,
            **data["algorithm"]["params"],
        )

        return self

    def plot_start_and_goal(self, ax) -> None:
        ax.plot(self.start.x, self.start.y, "go")
        ax.plot(self.goal.x, self.goal.y, "ro")