#!/usr/bin/env python3

import os
import matplotlib.pyplot as plt
from pathlib import Path
import argparse
from sys import path
import numpy as np

path.append("../csq")
from csq import CSQReader
import cv2


def export_thermal_image(frame):
    colormap = plt.cm.inferno
    norm = plt.Normalize(vmin=frame.min(), vmax=frame.max())
    image = colormap(norm(frame))
    return image


def v1(args):
    input_file = args.input_file
    output_video = args.output_video
    fps = float(args.fps)
    reader = CSQReader(input_file)
    video_writer = None
    sr = None

    if args.upscale_video is True:
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        sr.readModel("models/EDSR_x4.pb")
        sr.setModel("edsr", 4)

    while reader.next_frame() is not None:
        frame = reader.next_frame()
        if frame is not None:
            img = export_thermal_image(frame)

            if video_writer is None:
                height, width, _ = img.shape
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                video_writer = cv2.VideoWriter(
                    output_video, fourcc, fps, (int(width), int(height))
                )

            img = img[:, :, :3]  # remove alpha channel
            img = img[..., ::-1]  # flip channels (RGB to BGR)
            img = np.uint8(img * 255)
            
            if args.upscale_video is True:
                img = sr.upsample(img)

            video_writer.write(img)

    video_writer.release()


def v2(args):
    input_file = args.input_file
    output_video = args.output_video
    fps = float(args.fps)
    reader = CSQReader(input_file)
    video_writer = None

    reader._populate_list()
    for frame in reader.frames():
        img = export_thermal_image(frame)

        if video_writer is None:
            height, width, _ = img.shape
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            video_writer = cv2.VideoWriter(
                output_video, fourcc, fps, (int(width), int(height))
            )

        img = img[:, :, :3]  # remove alpha channel
        img = img[..., ::-1]  # flip channels (RGB to BGR)

        img = np.uint8(img * 255)
        video_writer.write(img)

    video_writer.release()


def main(args):
    v1(args)


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
        "--upscale_video",
        help="Increase the output video resolution using ai upscaling",
        type=bool,
        default=False,
    )
    args = parser.parse_args()

    # if input image path is invalid then stop
    assert os.path.isfile(args.input_file), "Invalid input file"

    # if output directory is invalid then stop
    if args.output_video:
        assert os.path.isdir(os.path.dirname(args.output_video)), "No such directory"

    main(args)
