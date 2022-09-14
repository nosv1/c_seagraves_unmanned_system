# let it be known the log parser used in this class is not very dynamic and 
# depends completley on the logging done in Dijkstra.py

import logging
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from Colors import Colors
from Logger import Logger
from Node import Node

class Plot:
    def plot_animation(fig: plt.Figure, ax: plt.Axes, animate=True, save_animation=True) -> None:
        """
        Plot the animation using the lines in the currently opened logger.
        :param fig: The figure to plot on.
        :param ax: The axes to plot on.
        """
        # close the open logger
        log_filename: str = logging.getLogger().handlers[0].baseFilename
        logging.info("Pausing for reading...")
        logging.shutdown()

        # read the log file
        with open(log_filename, "r") as f:
            lines = f.readlines()

        # restart logger
        Logger.start_logging()
        logging.info("Unpaused")

        # initialize the lines and objects we're going to plot
        path_line, = ax.plot([], [], "-", color=Colors.light_blue, linewidth=3)
        unvisted_neighbors_plot, = ax.plot([], [], "o", color=Colors.dark_green)
        visited_neighbors_plot, = ax.plot([], [], "o", color=Colors.dark_grey)
        invalid_neighbors_plot, = ax.plot([], [], "o", color=Colors.dark_red)
        current_nodes_plot = []

        # initialize the frames of the animation
        # these are the populated 'plt.Artist' objects,
        # basically every element in these lists is a plot
        neighbor_frames = []
        path_frames = []

        # initalize the lists where we'll temporarily store neighbor information
        # every iteration of dijkstra has a new set of neighbors
        unvisted_neighbors: list[tuple] = []
        visited_neighbors: list[tuple] = []
        invalid_neighbors: list[tuple] = []

        # the order of which we visit nodes and set them as current nodes
        current_nodes: list[Node] = []

        # we add additional plot frames for the path because we have to set a framerate
        # and interval between frames for the FuncAnimation. This means we can have 
        # a low interval between frames, speeding through the neighbors, but not the path.    
        path_frames_per_frame = 1

        # example parseable logger lines
        # INFO:root::Path:
        # INFO:root::Node:In obstacle: (4.00000, 0.00000)
        # INFO:root::Neighbors:Node:Visited Neighbor: (5.50000, 0.50000)

        # find the final attempt in the log...
        # we may have multiple attempts in the log because we sometimes re-generate
        # maps if a map is not solveable
        final_attempt_index = len(lines)
        i = final_attempt_index - 1
        while i >= 0:
            line = lines[i]
            if "Visiting all Nodes..." in line:
                final_attempt_index = i
                break
            i -= 1
        
        # parse the logger lines
        for line in lines[final_attempt_index:]:
            # the line that holds the list of node coords
            if ":Path:" in line:
                path_frames: list[tuple] = eval(f"[{line.split(':Path:')[1]}]")
                # loop backwards through the path frames, adding duplicates as desired
                i = len(path_frames) - 1
                while i >= 0:
                    for j in range(path_frames_per_frame - 1):  # adding the duplicate frames
                        path_frames.insert(i + 1, path_frames[i])
                    i -= 1

            # lines that deal with neighbors
            elif ":Neighbors:" in line:
                # on Discovering neighbors line, we reset the neighbor lists for the next frame
                if ":Discovering neighbors..." in line:
                    neighbor_frames.append(
                        {
                            "unvisted_neighbors": unvisted_neighbors.copy(),
                            "visited_neighbors": visited_neighbors.copy(),
                            "invalid_neighbors": invalid_neighbors.copy(),
                        }
                    )
                    unvisted_neighbors = []
                    visited_neighbors = []
                    invalid_neighbors = []

                elif ":Visited Neighbor:" in line:
                    visited_neighbors.append(eval(line.split(":Visited Neighbor:")[1]))

                elif ":Unvisted Neighbor:" in line:
                    unvisted_neighbors.append(eval(line.split(":Unvisted Neighbor:")[1]))

            elif ":Node:" in line:
                if ":In obstacle:" in line:
                    invalid_neighbors.append(eval(line.split(":In obstacle:")[1]))
                elif ":Out of bounds:" in line:
                    invalid_neighbors.append(eval(line.split(":Out of bounds:")[1]))
                elif ":Current Node:" in line:
                    current_nodes.append(eval(line.split(":Current Node:")[1].strip()))

        # combine the neighbors and path frames
        frames = neighbor_frames + path_frames

        def update(frame_number):
            """
            Update function for FuncAnimation. 
            Depending on the 'i', we know where we're at in the frame list, 
            so we know what to plot in which frame.
            :param frame_number: the current frame number
            """
            # neighbors frames go first
            if frame_number < len(neighbor_frames):
                # setting the x, y coords for each of the neighbor plots
                unvisted_neighbors_plot.set_data(
                    [n[0] for n in neighbor_frames[frame_number]["unvisted_neighbors"]],
                    [n[1] for n in neighbor_frames[frame_number]["unvisted_neighbors"]]
                )
                visited_neighbors_plot.set_data(
                    [n[0] for n in neighbor_frames[frame_number]["visited_neighbors"]],
                    [n[1] for n in neighbor_frames[frame_number]["visited_neighbors"]]
                )
                invalid_neighbors_plot.set_data(
                    [n[0] for n in neighbor_frames[frame_number]["invalid_neighbors"]],
                    [n[1] for n in neighbor_frames[frame_number]["invalid_neighbors"]]
                )
                # FIXME this makes plotting slow...
                current_nodes_plot.append(
                    ax.text(
                        current_nodes[frame_number].x,
                        current_nodes[frame_number].y,
                        f"{current_nodes[frame_number].total_cost:.1f}",
                        ha="center",
                        va="center",
                        color=Colors.light_grey,
                        fontsize=6
                    )
                )

                # we clear the plots we aren't showing in a given frame
                path_line.set_data([], [])

            # then path frames
            else:
                unvisted_neighbors_plot.set_data([], [])
                visited_neighbors_plot.set_data([], [])
                invalid_neighbors_plot.set_data([], [])
                path_line.set_data(
                    [n[0] for n in path_frames[:frame_number-len(neighbor_frames)]],
                    [n[1] for n in path_frames[:frame_number-len(neighbor_frames)]]
                )

            return (
                unvisted_neighbors_plot, 
                visited_neighbors_plot, 
                invalid_neighbors_plot,
                *current_nodes_plot,
                path_line,
            )

        # designing the plot
        fig.patch.set_facecolor(Colors.grey)
        ax.set_facecolor(Colors.grey)
        ax.title.set_color(Colors.light_grey)
        ax.xaxis.label.set_color(Colors.light_grey)
        ax.yaxis.label.set_color(Colors.light_grey)
        ax.tick_params(axis='x', colors=Colors.light_grey)
        ax.tick_params(axis='y', colors=Colors.light_grey)

        # setting the legend
        legend_elements = [
            Line2D([0], [0], marker='o', color=Colors.dark_grey, label='Obstacles', markerfacecolor=Colors.red, markersize=10),
            Line2D([0], [0], marker='o', color=Colors.dark_grey, label='Start', markerfacecolor=Colors.green, markersize=10),
            Line2D([0], [0], marker='o', color=Colors.dark_grey, label='Goal', markerfacecolor=Colors.white, markersize=10),
            Line2D([0], [0], color=Colors.light_blue, lw=4, label='Path'),
            Line2D([0], [0], marker='o', color=Colors.dark_grey, label='Unvisted Neighbors', markerfacecolor=Colors.dark_green, markersize=10),
            Line2D([0], [0], marker='o', color=Colors.dark_grey, label='Visited Neighbors', markerfacecolor=Colors.dark_grey, markersize=10),
            Line2D([0], [0], marker='o', color=Colors.dark_grey, label='Invalid Neighbors', markerfacecolor=Colors.dark_red, markersize=10),
        ]
        ax.legend(
            ncol=1,
            fancybox=True,
            shadow=True,
            handles=legend_elements, 
            loc='upper right'
        )

        if animate:
            # initalizing the animation
            animation = FuncAnimation(
                fig, 
                update, 
                frames=len(frames) + 10,
                repeat=True, 
                interval=100, blit=True
            )

            # save the animation
            if save_animation:
                animation.save(
                    "animation.gif", 
                    writer="Pillow", 
                    fps=10, 
                    progress_callback=lambda i, n: print(f"Saving frame {i} of {n}")
                )

        else:
            path_x = [n[0] for n in path_frames]
            path_y = [n[1] for n in path_frames]
            ax.plot(path_x, path_y, color=Colors.light_blue, lw=4)


        ax.set_aspect('equal', adjustable='box')
        fig.tight_layout()
        fig.set_size_inches(8, 8)

        # show the animiation
        plt.show()