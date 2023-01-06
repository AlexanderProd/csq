#!/bin/bash

INPUT=/Users/alexanderhoerl/Documents/FLIR\ Aufnahmen/Wildpark-3_2022-08-02/*
OUTPUT=/Users/alexanderhoerl/Documents/FLIR\ Export/Wildpark-3_2022-08-02/
TMP=/Users/alexanderhoerl/Downloads/tmp/

for FILE in /Users/alexanderhoerl/Documents/FLIR\ Aufnahmen/Wildpark-3_2022-08-02/*;
do
  FILENAME=$(basename "$FILE")
  echo "$FILENAME"
  python3 main.py "$FILE" "$TMP"
  ffmpeg -r 30 -f image2 -i $TMP"${FILENAME}"_%d.png -vcodec libx264 -crf 22 -pix_fmt yuv420p -vf 'scale=-2:min(1080\,trunc(ih/2)*2)' $OUTPUT"${FILENAME//.csq}".mp4
  rm "$TMP"*.png
done