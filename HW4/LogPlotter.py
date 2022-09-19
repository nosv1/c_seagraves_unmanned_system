import math
import matplotlib.pyplot as plt
import re

from Colors import Colors

def read_log_file(filename: str) -> list[str]:
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines

def plot_data(data: list[str]) -> None:
    # create two sub plots
    # one plot is an x y position graph where the color of the line is a funciton of the time
    # the other plot is a time vs. velocity graph

    current_t: list[float] = []
    current_x: list[float] = []
    current_y: list[float] = []
    current_z: list[float] = []
    current_roll: list[float] = []
    current_pitch: list[float] = []
    current_yaw: list[float] = []
    
    command_t: list[float] = []
    command_x: list[float] = []   # forward
    command_yaw: list[float] = []  # z in the angular vector

    start: float = None

    for line in data:

        # [INFO] [1663611139.413140100] [PID]: Position: [11.08, -1.38, 0.01]
        # [INFO] [1663611139.414072800] [PID]: Rotation: [-0.00, -0.01, -0.12, 0.99]
        # [INFO] [1663611139.414954200] [PID]: Publishing Linear: [0.00, 0.00, 0.00]
        # [INFO] [1663611139.416533000] [PID]: Publishing Angular: [0.00, 0.00, 0.00]
        
        point: list[float] = re.findall(r"-?\d*\.\d+|\d+", line)
        start = float(point[0]) if not start else start

        if "Position" in line:
            current_t.append(float(point[0]) - start)
            current_x.append(float(point[1]))
            current_y.append(float(point[2]))
            current_z.append(float(point[3])) 

        elif "Rotation" in line:
            current_roll.append(float(point[1]) * 180 / math.pi)
            current_pitch.append(float(point[2]) * 180 / math.pi)
            current_yaw.append(float(point[3]) * 180 / math.pi)

        # because we're not logging the current command every iteration, we 
        # dupliacte the last command and update the time so our plot is straight lines
        elif "Publishing Linear" in line:
            if command_x:
                command_x.append(command_x[-1])

            command_t += [float(point[0]) - start] * (2 if command_t else 1)
            command_x.append(float(point[1]))

        elif "Publishing Angular" in line:
            if command_yaw:
                command_yaw.append(command_yaw[-1])
            command_yaw.append(float(point[3]))

    fig = plt.figure()
    plt.style.use('dark_background')
    plt.set_cmap("Blues")
    position_subplot = plt.subplot2grid((3, 2), (0, 0), colspan=1)
    rotation_subplot = plt.subplot2grid((3, 2), (1, 0), colspan=1)
    command_subplot = plt.subplot2grid((3, 2), (2, 0), colspan=1)
    xy_subplot = plt.subplot2grid((3, 2), (0, 1), rowspan=3)

    twin_position = position_subplot.twinx()
    twin_command = command_subplot.twinx()

    fig.set_size_inches(9, 6)

    fig.set_facecolor(Colors.grey)
    for subplot in [
        position_subplot, 
        twin_position,
        rotation_subplot, 
        command_subplot, 
        twin_command,
        xy_subplot,
    ]:
        subplot.set_facecolor(Colors.grey)
        subplot.title.set_color(Colors.light_grey)
        subplot.xaxis.label.set_color(Colors.light_grey)
        subplot.yaxis.label.set_color(Colors.light_grey)
        subplot.tick_params(colors=Colors.light_grey)
    
    position_subplot.set_title("Position")
    rotation_subplot.set_title("Rotation")
    command_subplot.set_title("Commands")
    xy_subplot.set_title("XY Position")

    # plotting
    position_subplot.plot(current_t, current_x, color=Colors.red, label="x")
    twin_position.plot(current_t, current_y, color=Colors.blue, label="y")

    rotation_subplot.plot(current_t, current_yaw, color=Colors.red, label="yaw")

    command_subplot.plot(command_t, command_x, color=Colors.red, label="x", marker="o")
    twin_command.plot(command_t, command_yaw, color=Colors.blue, label="yaw", marker="o")

    xy_subplot.scatter(current_x, current_y, c=current_t, label="xy")

    min_axis = min(min(current_x), min(current_y)) - 0.5
    max_axis = max(max(current_x), max(current_y)) + 0.5
    xy_subplot.set_xlim(min_axis, max_axis)
    xy_subplot.set_ylim(min_axis, max_axis)
    xy_subplot.set_aspect('equal')
    
    # labels
    position_subplot.set_ylabel('x (m)')
    twin_position.set_ylabel('y (m)', rotation=270, labelpad=15)

    rotation_subplot.set_ylabel('yaw (deg)')

    command_subplot.set_xlabel('time (s)')
    command_subplot.set_ylabel('x (m/s)')
    twin_command.set_ylabel('yaw (rad/s)', rotation=270, labelpad=15)

    xy_subplot.set_xlabel('x (m)')
    xy_subplot.set_ylabel('y (m)')

    # legends
    position_subplot.legend(loc='upper left')
    twin_position.legend(loc='upper right')
    rotation_subplot.legend(loc='upper left')
    command_subplot.legend(loc='upper left')
    twin_command.legend(loc='upper right')
    xy_subplot.legend()

    # plot colorbar for xy subplot
    cbar = plt.colorbar(xy_subplot.collections[0], ax=xy_subplot)
    cbar.set_label('time (s)')
    cbar.ax.yaxis.label.set_color(Colors.light_grey)
    cbar.ax.tick_params(colors=Colors.light_grey)

    plt.show()

def main() -> None:
    log_lines: list[str] = read_log_file("Logs/log.log")
    plot_data(log_lines)

if __name__ == "__main__":
    main()
