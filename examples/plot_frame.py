#!/usr/bin/env python3

from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.pyplot as plt
from sys import argv, path

path.append("../csq")
from csq import CSQReader


file_path = argv[1]
reader = CSQReader(file_path)


def plot_thermal(frame):

    ax = plt.gca()
    plt.axis("off")
    im = plt.imshow(frame, cmap="inferno")
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = plt.colorbar(im, cax=cax)
    cbar.ax.set_ylabel("Temperature ($^{\circ}$C)", fontsize=14)
    plt.show()


frame = reader.frame_at(0)
plot_thermal(frame)
