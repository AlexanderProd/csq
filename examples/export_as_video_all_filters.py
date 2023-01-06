#!/usr/bin/env python3

import matplotlib.pyplot as plt
from pathlib import Path
from sys import argv, path
import os
import numpy as np

path.append("../csq")
from csq import CSQReader
from colormaps import green_hot, cold_green, red_hot, cold_red, ironbow
import cv2


file_path = argv[1]
output = argv[2]
input_filename = Path(file_path).name
reader = CSQReader(file_path)


filters = [
    "hot",
    "cool",
    "jet",
    "gray_r",
    "gray",
]


def export_thermal_image(frame, filter=plt.cm.hot):
    norm = plt.Normalize(vmin=frame.min(), vmax=frame.max())

    colormap = filter
    if type(filter) == str:
        colormap = plt.colormaps[filter]

    image = colormap(norm(frame))
    return image


def render_video(output_filename: str, filter):
    video_writer = None

    reader._populate_list()
    for frame in reader.frames():
        img = export_thermal_image(frame, filter)

        if video_writer is None:
            height, width, _ = img.shape
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video_writer = cv2.VideoWriter(
                output_filename, fourcc, 30.0, (int(width), int(height))
            )

        img = img[:, :, :3]  # remove alpha channel
        img = img[..., ::-1]  # flip channels (RGB to BGR)

        img = np.uint8(img * 255)
        video_writer.write(img)


def main():
    if not os.path.isdir(output):
        print("The provided output path is not a directory.")
        os.exit(1)

    for filter in filters:
        output_filename = output + input_filename + "_" + filter + ".mp4"
        print(output_filename)
        render_video(output_filename, filter)


main()
