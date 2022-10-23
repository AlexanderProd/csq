#!/usr/bin/env python3

import matplotlib.pyplot as plt
from pathlib import Path
from sys import argv, path
import numpy as np

path.append("../csq")
from csq import CSQReader
import cv2

file_path = argv[1]
output = argv[2]
input_filename = Path(file_path).name
reader = CSQReader(file_path)


def export_thermal_image(frame):
    colormap = plt.cm.hot
    norm = plt.Normalize(vmin=frame.min(), vmax=frame.max())
    image = colormap(norm(frame))
    return image


def main():
    video_writer = None

    reader._populate_list()
    for frame in reader.frames():
        img = export_thermal_image(frame)

        if video_writer is None:
            height, width, _ = img.shape
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video_writer = cv2.VideoWriter(
                output, fourcc, 30.0, (int(width), int(height))
            )

        img = img[:, :, :3]  # remove alpha channel
        img = img[..., ::-1]  # flip channels (RGB to BGR)

        img = np.uint8(img * 255)
        video_writer.write(img)

    video_writer.release()


main()
