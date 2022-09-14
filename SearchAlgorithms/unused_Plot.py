import matplotlib.pyplot as plt

from Colors import Colors

class Plot:
    def setup_plot():
        fig, ax = plt.subplots()
        fig.patch.set_facecolor(Colors.grey)
        ax.set_facecolor(Colors.grey)
        ax.title.set_color(Colors.light_grey)
        ax.xaxis.label.set_color(Colors.light_grey)
        ax.yaxis.label.set_color(Colors.light_grey)
        ax.tick_params(axis='x', colors=Colors.light_grey)
        ax.tick_params(axis='y', colors=Colors.light_grey)
