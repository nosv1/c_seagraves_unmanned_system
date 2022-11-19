import matplotlib.pyplot as plt
import numpy as np

from PythonRobotics.PathPlanning.DubinsPath import dubins_path_planner as dpp
from PythonRobotics.utils import plot

if __name__ == "__main__":
    start_x = 1.0
    start_y = 1.0
    start_yaw = np.deg2rad(45.0)
    end_x = 0.0
    end_y = 0.0
    end_yaw = np.deg2rad(45 + 90)
    curvature = 6.8
    diameter = 1.0 / curvature
    radius = diameter / 2.0
    print(diameter, radius)
    step_size = 0.1
    path_x, path_y, path_yaw, mode, _ = dpp.plan_dubins_path(
        start_x,
        start_y,
        start_yaw,
        end_x,
        end_y,
        end_yaw,
        curvature,
        step_size
    )
    plt.plot(path_x, path_y, label="".join(mode))
    plot.plot_arrow(start_x, start_y, start_yaw)
    plot.plot_arrow(end_x, end_y, end_yaw)
    plt.grid(True)
    plt.axis("equal")
    plt.legend()
    plt.show()

