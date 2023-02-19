#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from sys import argv, path
import os
from matplotlib.colors import LinearSegmentedColormap

path.append("../csq")
from colormaps import green_hot, cold_green, red_hot, cold_red, ironbow, hottest
from export_as_video import v1 as render_video


file_path = argv[1]
output = argv[2]
input_filename = Path(file_path).name

filters: list[LinearSegmentedColormap | str] = [
    green_hot,
    cold_green,
    red_hot,
    cold_red,
    ironbow,
    hottest,
    "hot",
    "cool",
    "jet",
    "gray_r",
    "gray",
]


def main():
    if not os.path.isdir(output):
        print("The provided output path is not a directory.")
        os.exit(1)

    for filter in filters:
        filtername: str = ""
        if type(filter) == str:
            filtername = filter

        if type(filter) == LinearSegmentedColormap:
            filtername = filter.name

        output_filename = output + input_filename + "_" + filtername + ".mp4"
        print(output_filename)
        render_video(input_file=file_path, output_video=output_filename, filter=filter)


main()
