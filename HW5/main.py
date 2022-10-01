from __future__ import annotations

from itertools import permutations
import matplotlib.pyplot as plt
from os import urandom

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @property
    def key(self) -> str:
        return f"({self.x:.5f}, {self.y:.5f})"

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

    def plot(self, color: str, linewidth=2):
        x = [point.x for point in self.path]
        y = [point.y for point in self.path]
        plt.plot(x, y, 'o-', color=color, label=f"Distance: {self.distance:.2f}", linewidth=linewidth)

class TSP:
    def __init__(self, points: list[Point]) -> None:
        self.points = points

        self.distance_matrix: dict[str, dict[str, float]] = self._create_distance_matrix()

    def _create_distance_matrix(self) -> dict:
        matrix: dict[str, dict[str, float]] = {}
        for point in self.points:
            matrix[point.key] = {}
            for other in self.points:
                matrix[point.key][other.key] = point.distance_to(other)
        return matrix

    def shortest_path(self, start: Point) -> Path:
        min_path: Path = Path()

        permutations_list = list(permutations(self.points))
        for permutation in permutations_list:
            if permutation[0] != start:
                continue
            
            path = Path(permutation)
            path.plot(color=f"#{hex(int.from_bytes(urandom(3), 'big'))[2:]:0>6}")
            min_path = path if path.distance < min_path.distance else min_path
        
        return min_path

def main():
    points: list[Point] = [
        Point(x=0, y=0),
        Point(x=2, y=2),
        Point(x=5, y=3),
        Point(x=3, y=4),
        Point(x=6, y=4)
    ]
    tsp: TSP = TSP(points)
    shortest_path: Path = tsp.shortest_path(start=points[0])
    for point in shortest_path.path:
        print(point)
    print(f"Distance: {shortest_path.distance:.2f}")

    shortest_path.plot(color="blue", linewidth=3)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    main()