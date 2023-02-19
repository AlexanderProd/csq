# csq

This repository provides a way for thermal videos acquired by a FLIR camera to be read in Python. Only files with the `.csq` extension are compatible with this code.

The `.csq` file format stores each image in the thermal video in 16-bit binary form. Using some calibration constants from the thermal camera, the temperature data can be calculated, allowing the image to be expressed in degrees Celcius. With this repository, you can directly obtain the temperature values without having to worry about this conversion!

## Installation

```
pip install -r requirements.txt
```

## Tutorial

Here I will use an example thermal video to show you how to use this repository. If you would like to follow along, you can download `cat.csq` from this Google Drive folder: https://drive.google.com/drive/folders/1aT98zkNw8DwJ1ImS4mUrWMhvL5NjCS7S?usp=sharing.

First, import the module and construct a CSQReader object from the path to `cat.csq`:

```python
from csq import CSQReader

path = '/Users/tuthill/Downloads/analysis/videos/cat.csq'
reader = CSQReader(path)
```

To read a frame of the video, you can use the `next_frame()` function. Let's read and plot the first frame:

```python
import seaborn as sns
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

def plot_thermal(frame):

    sns.set_style('ticks')
    fig = plt.figure()
    ax = plt.gca()
    im = plt.imshow(frame, cmap = 'hot')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.05)
    cbar = plt.colorbar(im, cax = cax)
    cbar.ax.set_ylabel('Temperature ($^{\circ}$C)', fontsize = 14)
    sns.despine()
    plt.show()

frame = reader.next_frame()
plot_thermal(frame)
```

![cat](https://github.com/katierupp/csq/blob/main/examples/frame1.png?raw=true)

When analyzing thermal imaging data, you may want to perform a certain operation on each frame. For example, maybe you want to extract the maximum temperature at each frame in the video. To determine this, you can simply create a loop to continuously call the `next_frame()` function:

```python
import numpy as np

max_temps = []

while reader.next_frame() is not None:
    frame = reader.next_frame()
    max_temps.append(np.max(frame))
    # other operations for current frame
```

However, there may be cases when you only need to extract thermal data from only certain frames within a video. For faster processing, you can use the `frame_at()` function to get the thermal data from a specific frame. Perhaps we only want to plot the 200th frame:

```python
frame = reader.frame_at(200)
plot_thermal(frame)
```

If you want to know how many frames a video has you can use the `count_frames()` function, it returns the number of frames as interger.

```python
print(reader.count_frames())
```

## Examples

There are some examples of use cases for exporting the CSQ files in different means in the `examples` directory.

### Export all frames

If you want to export all frames of a CSQ file as individual files automatically. An full example is also located in the examples directory of this repo.

```python
def export_thermal_image(frame, name: str):
    filen_name = output + name + ".png"
    hot = plt.cm.hot
    norm = plt.Normalize(vmin=frame.min(), vmax=frame.max())
    image = hot(norm(frame))
    plt.imsave(filen_name, image)


i = 0
reader._populate_list()
for frame in reader.frames():
    export_thermal_image(frame, name="filename_" + str(i))
    i += 1
```

### Export as Video

The `export_as_video.py` file located in the `examples` directory can be used to export a CSQ as a video file. It has a flag to set the framerate of the video, the default is 30 fps.

```bash
$ python3 examples/export_as_video.py -i example.csq -o output.mp4 --fps 30
```

### Export as video all filters

This examples exports a CSQ file as video files with different thermal filters. The first argument needs to be the input CSQ file and the second one an output directory.

```bash
    python3 examples/export_as_video_all_filters.py ~/Documents/FLIR\ Aufnahmen/Erlangen_Wildschweingehege_2022-07-21/FLIR0115.csq ~/Downloads/FLIR0115/
```

### Super Resolution

To use the AI upscaling feature you have to download a tensorflow model from one of theses sources and edit the `export_as_video.py` file as well as setting the `--upscale_video` flag to true.

- https://github.com/Saafke/EDSR_Tensorflow/tree/master/models
- https://github.com/fannymonori/TF-LapSRN/tree/master/export

## References

This project was inspired by the Thermimage package, which allows for FLIR thermal image analysis in R:

Glenn J. Tattersall. (2017, December 3). Thermimage: Thermal Image Analysis. doi: 10.5281/zenodo.1069704 (URL:<http://doi.org/10.5281/zenodo.1069704>), R package, &lt;URL:<https://CRAN.R-project.org/package=Thermimage>&gt;.[![DOI](https://zenodo.org/badge/33262273.svg)](https://zenodo.org/badge/latestdoi/33262273)
