from __future__ import annotations

from itertools import permutations
from math import factorial
import matplotlib.pyplot as plt
from multiprocessing import Pool
from os import urandom
from random import random
from time import perf_counter

def create_path(path: tuple[Point]) -> Path:
    return Path(path=path)

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @property
    def key(self) -> tuple(float, float):
        return (self.x, self.y)

    def __str__(self):
        return f"({self.x:.2f}, {self.y:.2f})"

    def point_from_key(key: str) -> Point:
        x, y = key.strip("()").split(",")
        return Point(float(x), float(y))

    def distance_to(self, other: Point) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

class Path:
    def __init__(self, path: tuple[Point]=()) -> None:
        self.path = path

        self.get_distance()

    def get_distance(self):
        self.distance: float = 0.0
        for i, point in enumerate(self.path):
            if not i:
                continue
            self.distance += point.distance_to(self.path[i - 1])
        self.distance = self.distance if self.distance else float('inf')

    def plot(self, color: str, linestyle="--", text_points=False):
        x = [point.x for point in self.path]
        y = [point.y for point in self.path]
        plt.plot(x, y, marker="o", color=color, linestyle=linestyle, alpha=0.3, label=f"Distance: {self.distance:.2f}")
        if text_points:
            for i, point in enumerate(self.path):
                plt.text(point.x+.15, point.y+.15, f"{i+1}: {point}", ha="center", va="center", bbox=dict(facecolor='white', alpha=0.85))

class TSP:
    def __init__(self, points: list[Point]) -> None:
        self.points = points

        self.distance_matrix: dict[str, dict[str, float]] = self._create_distance_matrix()

    def _create_distance_matrix(self) -> dict:
        print("Creating distance matrix...")

        matrix: dict[str, dict[str, float]] = {}
        for point in self.points:
            matrix[point.key] = {}
            for other in self.points:
                matrix[point.key][other.key] = point.distance_to(other)
        return matrix

    def top_paths(self, start: Point, count: int=1) -> tuple[Path]:

        # if we knew start was [0] slicing could be faster
        points = [point for point in self.points if point.key != start.key]

        start_time: float = perf_counter()
        print(f"Generating {factorial(len(points)):,} permutations...", end=" ")
        path_permutations: list[tuple[Point]] = list(permutations(points))
        print(f"{perf_counter() - start_time:.2f}s")

        start_time: float = perf_counter()        
        print("Calculating distances...", end=" ")
        paths: list[Path] = None
        with Pool() as pool:
            paths = pool.map(create_path, path_permutations)
            print(f"{perf_counter() - start_time:.2f}s")

        start_time: float = perf_counter()
        print(f"Finding top {count} path(s)...", end=" ")
        top_paths: list[Path] = [Path() for _ in range(count)]
        for path in paths:
            path.distance = (
                path.distance +
                self.distance_matrix[start.key][path.path[0].key]
            )
            for i, short_path in enumerate(top_paths):
                if path.distance < short_path.distance:
                    top_paths.insert(i, path)
                    top_paths.pop()
                    break
                    
        print(f"{perf_counter() - start_time:.2f}s")
        return top_paths

def main():
    print("Getting points...")
    points: list[Point] = [
        Point(x=0, y=0),
        Point(x=2, y=2),
        Point(x=5, y=3),
        Point(x=3, y=4),
        Point(x=6, y=4)
    ]

    points: list[Point] = []
    min_axes: float = 0.0
    max_axes: float = 20.0
    for i in range(10):  ## input number of points here, more than 11 is slow
        points.append(Point(x=random() * max_axes, y=random() * max_axes))

    tsp: TSP = TSP(points)

    print(f"Finidng shortest path (Points: {len(tsp.points)})...")
    top_paths: tuple[Path] = tsp.top_paths(start=points[0], count=2)
    for i, path in enumerate(top_paths):
        for point in path.path:
            print(point)
        print(f"Distance: {path.distance:.2f}")
        color = f"#{urandom(3).hex()}"
        path.plot(
            color="blue" if not i else color,
            linestyle="-" if not i else "--",
            text_points=not i
        )

    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()