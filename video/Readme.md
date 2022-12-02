### This directory contains two scripts that serves for video files handling:

***slicer.py***

> This script takes a path to a directory containing video files and cuts each video file frame by frame. All the frames of a video are stored in a corresponding directory. A possible option is to save one frame each second of the video.

**Arguments:**

- path_to_videos: str - path to the directory containing video files

- ouptut_path: str - path to the directory where the folders with corresponding frames will be stored

- slicing_type: str ['frames', 'seconds'] - flag that helps the user to control logic of saving video frames

- num_process: int - number of the processes that will handle videos, if __None__ argument is provided all logical cores will be used



***combiner:***

> This script takes a path to a directory containing video files and creates the resulting video where all input videos are combined into a grid of a square shape. Size of the grid will be counted automatically based on the number of images. The spare space in the grid will be filled with black images.

**Arguments:**

- path_to_videos: str - path to the directory containing video files

- output_video: str - path to and name of the file where the resulting video file will be saved
