#!/usr/bin/env python3
from __future__ import annotations

import os
import matplotlib.pyplot as plt
from pathlib import Path
import argparse
from sys import path
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import time
from colormaps import green_hot, cold_green, red_hot, cold_red, ironbow, hottest

path.append("../csq")
from csq import CSQReader
import cv2


def extract_dnn_model_name_and_scale(model_path: Path) -> tuple[str, int]:
    model_name = model_path.split(os.path.sep)[-1].split("_")[0].lower()
    model_scale = model_path.split("_x")[-1]
    model_scale = int(model_scale[: model_scale.find(".")])
    return model_name, model_scale


def export_thermal_image(frame, filter: LinearSegmentedColormap | str):
    norm = plt.Normalize(vmin=frame.min(), vmax=frame.max())

    colormap = filter
    if type(filter) == str:
        colormap = plt.colormaps[filter]

    image = colormap(norm(frame))
    return image


def v1(
    input_file: Path,
    output_video: Path,
    fps: int | float = 30,
    sr: cv2.dnn_superres.DnnSuperResImpl = None,
    scaling_factor: int = 1,
    filter: LinearSegmentedColormap | str = "ironbow",
):
    fps = float(fps)
    reader = CSQReader(input_file)
    video_writer = None

    while reader.next_frame() is not None:
        frame = reader.next_frame()
        if frame is not None:
            img = export_thermal_image(frame, filter)

            if video_writer is None:
                height, width, _ = img.shape
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                video_writer = cv2.VideoWriter(
                    output_video,
                    fourcc,
                    fps,
                    (int(width * scaling_factor), int(height * scaling_factor)),
                )

            img = img[:, :, :3]  # remove alpha channel
            img = img[..., ::-1]  # flip channels (RGB to BGR)
            img = np.uint8(img * 255)

            if sr is not None:
                img = sr.upsample(img)

            video_writer.write(img)

    video_writer.release()


def v2(
    input_file: Path,
    output_video: Path,
    fps: int | float = 30,
    sr: cv2.dnn_superres.DnnSuperResImpl = None,
    scaling_factor: int = 1,
    filter: LinearSegmentedColormap | str = "hot",
):
    reader = CSQReader(input_file)
    video_writer = None

    reader._populate_list()
    for frame in reader.frames():
        img = export_thermal_image(frame, filter)

        if video_writer is None:
            height, width, _ = img.shape
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video_writer = cv2.VideoWriter(
                output_video,
                fourcc,
                fps,
                (int(width * scaling_factor), int(height * scaling_factor)),
            )

        img = img[:, :, :3]  # remove alpha channel
        img = img[..., ::-1]  # flip channels (RGB to BGR)
        img = np.uint8(img * 255)

        if sr is not None:
            img = sr.upsample(img)

        video_writer.write(img)

    video_writer.release()


def main(args):
    start = time.time()
    sr = None
    scaling_factor = 1

    if args.dnn_model is not None:
        print(args.dnn_model)
        print("Upscaling video output")
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        sr.readModel(args.dnn_model)
        sr.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        sr.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        model_name, scaling_factor = extract_dnn_model_name_and_scale(args.dnn_model)
        sr.setModel(model_name, scaling_factor)
        scaling_factor = scaling_factor

    v2(
        input_file=args.input_file,
        output_video=args.output_video,
        scaling_factor=scaling_factor,
        filter=ironbow,
        fps=args.fps,
        sr=sr,
    )
    end = time.time()
    print("\n Exporting video took {:.6f} seconds".format(end - start))


if __name__ == "__main__":
    # creating argument parser

    parser = argparse.ArgumentParser(description="Video rendering parameters")
    parser.add_argument(
        "-i", "--input_file", help="Path to your .csq file.", type=str, required=True
    )
    parser.add_argument("-o", "--output_video", help="Output file path", type=str)
    parser.add_argument(
        "--fps",
        help="Frames per second of the video file.",
        type=float,
        default=30.0,
    )
    parser.add_argument(
        "--dnn_model",
        help="Path to the DNN model to use for upscaling.",
        type=str,
    )
    args = parser.parse_args()

    # if input image path is invalid then stop
    assert os.path.isfile(args.input_file), "Invalid input file"

    # if output directory is invalid then stop
    if args.output_video:
        assert os.path.isdir(os.path.dirname(args.output_video)), "No such directory"

    main(args)
