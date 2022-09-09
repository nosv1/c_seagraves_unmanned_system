from __future__ import annotations
import json
import matplotlib.pyplot as plt
import random

from AStar import AStar
from RRT import RRT
from Grid import Grid
from Node import Node
from Obstacle import Obstacle

class Scenario:
    def loader(self, filename) -> Scenario:
        with open(filename) as f:
            data = json.load(f)
            
        for key in data:
            if key == "bot_radius":
                self.bot_radius = data[key]

            elif key == "grid":
                self.grid: Grid = Grid(
                    min_x=data[key]["min_x"],
                    max_x=data[key]["max_x"],
                    min_y=data[key]["min_y"],
                    max_y=data[key]["max_y"],
                    grid_spacing=data[key]["grid_spacing"],
                    obstacles=[]
                )

            elif key == "obstacles":
                self.obstacle_radius = data[key]["radius"]

                if "file" in data[key]:
                    self.obstacles = Obstacle.obstacles_from_file(
                        filename=data[key]["file"], 
                        radius=float(self.obstacle_radius)
                    )

                else:
                    self.obstacles = Obstacle.generate_obstacles(
                        count=data[key]["count"],
                        radius=self.obstacle_radius,
                        min_x=self.grid.min_x,
                        max_x=self.grid.max_x,
                        min_y=self.grid.min_y,
                        max_y=self.grid.max_y
                    )
                    for obstacle in list(self.obstacles.values()):
                        del self.obstacles[obstacle.id]
                        obstacle: Node = self.grid.snap_node_to_grid(obstacle)
                        self.obstacles[obstacle.id] = obstacle

                self.grid.obstacles = self.obstacles
                self.grid.inflate_obstacles(self.bot_radius)
                self.grid.inflate_bounds(self.bot_radius)
                self.grid.set_nodes()

            elif key == "start":
                if data[key] == "random":
                    self.start = self.grid.generate_valid_node()

                else:
                    self.start: Node = Node(
                        x=float(data[key]["x"]),
                        y=float(data[key]["y"])
                    )

            elif key == "goal":
                if data[key] == "random":
                    self.goal = self.grid.generate_valid_node()

                else:
                    self.goal: Node = Node(
                        x=float(data[key]["x"]),
                        y=float(data[key]["y"])
                    )

            elif key == "algorithm":
                self.algorithm: RRT | AStar = eval(data[key]["type"])(
                    start=self.start,
                    goal=self.goal,
                    grid=self.grid,
                    **data["algorithm"]["params"],
                )

        return self

    def plot_start_and_goal(self, ax) -> None:
        ax.plot(self.start.x, self.start.y, "go")
        ax.plot(self.goal.x, self.goal.y, "ro")