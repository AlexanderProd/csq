import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.widgets import Button
from mpl_toolkits.axes_grid1 import make_axes_locatable
from pathlib import Path
from sys import argv

from csq import CSQReader

path = argv[1]
output = argv[2]
filename = Path(path).name

# Colors in RGB Percent
ironbow = LinearSegmentedColormap.from_list(
    "Ironbow",
    [(0, 0, 0), (0.13, 0, 0.55), (0.8, 0, 0.47), (1, 0.84, 0), (1, 1, 1)],
    N=100,
)
red_green_blue = LinearSegmentedColormap.from_list(
    "Red Green Blue", [(1, 0, 0), (0, 1, 0), (0, 0, 1)], N=200
)
cold_green = LinearSegmentedColormap.from_list(
    "Cold Green", [(0, 0.76, 0), (0, 0, 0)], N=100
)
green_hot = LinearSegmentedColormap.from_list(
    "Cold Green", [(0, 0, 0), (0, 0.76, 0)], N=100
)
cold_green_boost = LinearSegmentedColormap.from_list(
    "Cold Green", [(0, 0.76, 0), (0, 0.3, 0), (0, 0, 0)], N=100
)


class CSQViewer:
    def __init__(self, path):
        self.path = path
        self.reader = CSQReader(self.path)

    def previous_frame(self, event):
        print(event)
        print("previous")

    def plot_thermal(self):

        ax = plt.gca()
        plt.axis("off")
        im = plt.imshow(self.reader.next_frame(), cmap="inferno")
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        cbar = plt.colorbar(im, cax=cax)
        cbar.ax.set_ylabel("Temperature ($^{\circ}$C)", fontsize=14)
        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        bprev = Button(axprev, "Previous")
        bprev.on_clicked(self.previous_frame)
        bnext = Button(axnext, "Next")
        bnext.on_clicked(print("next"))
        plt.show()

    def export_thermal_image(frame, name: str, color_map="Greys_r"):
        fname = output + name + ".png"
        hot = plt.cm.hot
        norm = plt.Normalize(vmin=frame.min(), vmax=frame.max())
        image = green_hot(norm(frame))
        plt.imsave(fname, image)


""" frame = reader.next_frame()
for color_map in plt.colormaps(): 
    print(color_map)
    export_thermal(frame, color_map) """

""" 
def export_all_frames(frame, i=0):
    export_thermal_image(frame, name=filename, frameNumber=str(i))
    export_all_frames(reader.next_frame(), i + 1)

 """

""" 
frame = reader.next_frame()
export_all_frames(frame)
"""

# v1
""" 
i = 0
while reader.next_frame() is not None:
    frame = reader.next_frame()
    if frame is not None:
        export_thermal_image(frame, name=filename + "_" + str(i))
        i += 1
 """
# v2

i = 0
reader._populate_list()
for frame in reader.frames():
    export_thermal_image(frame, name=filename + "_" + str(i))
    i += 1


csq_viewer = CSQViewer(path)
csq_viewer.plot_thermal()

""" 
reader._populate_list()
# print(reader.count_frames())
# frame = reader.frame_at(0)
# export_thermal_image(frame, name=filename + "_black_hot_" + str(0))
frame = reader.next_frame()
plot_thermal(frame)
 """

""" print(reader.count_frames()) """
