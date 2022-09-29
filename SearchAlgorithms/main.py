# Simply uncomment a scenario at the top of main() and run it.
# Scenario's are loaded via ./Scenario.Scenario.loader()

from matplotlib.lines import Line2D
import matplotlib.pyplot as plt

from Colors import Colors
from Scenario import Scenario

def main() -> None:
    scenario: Scenario = Scenario().loader(
        #####  the naming structure for scenarios  #####
        # "scenarios / SearchType _ grid-size _ bot-size _ grid-spacing.json"
        # "scenarios/AStar_10x10_bot-0o5_grid-0o5.json"  --> -->
        # "scenarios / AStar _ 10x10 grid _ bot radius 0.5 _ grid spacing 0.5"
        # if 'random' is at the end, then random start/goal pos and/or obstacle pos
        #####

        #####  scenarios in the "scenarios" folder  #####
        # "scenarios/AStar_10x10_bot-0o5_grid-0o5.json"
        # "scenarios/AStar_10x10_bot-0o5_grid-0o5_random.json"
        "scenarios/AStar_15x15_bot-0o5_grid-1o0.json"        # HW5 problem 1a
        # "scenarios/AStar_50x50_bot-0o5_grid-0o5.json"        # HW3 problem 2
        # "scenarios/AStar_50x50_bot-0o5_grid-0o5_random.json"
        # "scenarios/Dijkstra_15x15_bot-0o5_grid-1o0.json"     # HW5 problem 1b
        # "scenarios/RRT_10x10_bot-0o5_grid-0o5.json"
        # "scenarios/RRT_10x10_bot-0o5_grid-0o5_random.json"
        # "scenarios/RRT_15x15_bot-0o5_grid-1o0.json"          # HW5 problem 1c
        # "scenarios/RRT_50x50_bot-0o5_grid-0o5.json"          # HW3 problem 3
        #####
    )

    # we setup the plot before we find the path for debugging - if we want to 
    # plot while the algorithm is running.
    print("Setting up plot...")
    fig, ax = plt.subplots()
    fig.set_size_inches(8, 8)
    
    # set colors
    fig.patch.set_facecolor(Colors.grey)
    ax.set_facecolor(Colors.grey)
    ax.title.set_color(Colors.light_grey)
    ax.xaxis.label.set_color(Colors.light_grey)
    ax.yaxis.label.set_color(Colors.light_grey)

    # set axis labels
    ax.tick_params(axis='x', colors=Colors.light_grey)
    ax.tick_params(axis='y', colors=Colors.light_grey)

    # set title
    ax.set_title(
        f"{scenario.algorithm.__class__.__name__}\n"
        f"Time: TBD, Cost: TBD"
    )

    # set axis limits
    ax.set_xlim(
        scenario.grid.min_x - scenario.grid.grid_spacing * 2, 
        scenario.grid.max_x + scenario.grid.grid_spacing * 2
    )
    ax.set_ylim(
        scenario.grid.min_y - scenario.grid.grid_spacing * 2, 
        scenario.grid.max_y + scenario.grid.grid_spacing * 2
    )

    print("Plotting legend...")
    ax.legend(
        handles=[
            Line2D([0], [0], marker='o', markersize=10, color=Colors.red, lw=4, label="Obstacles"),
            Line2D([0], [0], marker='o', markersize=10, color=Colors.light_purple, lw=4, label="Open Set"),
            Line2D([0], [0], marker='o', markersize=10, color=Colors.light_grey, lw=4, label="Closed Set"),
            Line2D([0], [0], color=Colors.light_blue, lw=4, label="Path"),
            Line2D([0], [0], marker='o', markersize=10, color="g", lw=4, label="Start"),
            Line2D([0], [0], marker='o', markersize=10, color="r", lw=4, label="Goal"),
        ],
        fancybox=True,
        shadow=True,
        loc="upper right"
    )
    # print("Plotting obstacles")
    # scenario.plot_obstacles(ax, Colors.red)
    print("Plotting nodes...")
    scenario.plot_nodes(ax, invalid_nodes=True, valid_nodes=False)
    print("Plotting start and goal...")
    scenario.plot_start_and_goal(ax)

    # find a path
    # if we use random start/goal, we make sure they're are valid, otherwise we
    # try again. We also try again if the path fails or is not long enough to be 
    # interesting - at the time of writing this, the path must be 2/3 of the 
    # width of the grid.
    while True:
        if (
            (scenario.has_random_start or scenario.has_random_goal) and 
            scenario.start.distance_to(scenario.goal) < scenario.grid.max_x / 1.5
        ):
            print("Start and goal not interesting enough... Regenerating...")
            plt.close()
            main()
            return

        try:
            print("Finding path...")
            scenario.algorithm.stopwatch.start()
            scenario.algorithm.find_path()
            scenario.algorithm.stopwatch.stop()
            print(f"Path found... Time: {scenario.algorithm.stopwatch.elapsed_time:.5f}s")
            break

        except ValueError:
            print("No path found... Regenerating...")
            plt.close()
            main()
            return

    # set title
    ax.set_title(
        f"{scenario.algorithm.__class__.__name__}\n"
        f"Time: {scenario.algorithm.stopwatch.elapsed_time:.3f}s, Cost: {scenario.algorithm._path[0].total_cost:.2f}"
    )

    print("Plotting open set...")
    scenario.plot_open_set(ax, color=Colors.light_purple)
    print("Plotting closed set...")
    scenario.plot_closed_set(ax, Colors.light_grey)
    print("Plotting path...")
    scenario.plot_path(ax, Colors.light_blue)

    print("Showing plot...")
    # using plt.pause for debugging, plt.show wasn't working when I was using
    # plt.pause within the algorithm classes
    plt.pause(1000)

if __name__ == "__main__":
    main()