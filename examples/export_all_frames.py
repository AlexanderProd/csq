#!/usr/bin/env python3

import matplotlib.pyplot as plt
from pathlib import Path
from sys import argv, path

path.append("../csq")
from csq import CSQReader

file_path = argv[1]
output = argv[2]
filename = Path(file_path).name
reader = CSQReader(file_path)


def export_thermal_image(frame, name: str):
    filen_name = output + name + ".png"
    hot = plt.cm.hot
    norm = plt.Normalize(vmin=frame.min(), vmax=frame.max())
    image = hot(norm(frame))
    plt.imsave(filen_name, image)


i = 0
reader._populate_list()
for frame in reader.frames():
    export_thermal_image(frame, name=filename + "_" + str(i))
    i += 1
