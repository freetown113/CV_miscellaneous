from argparse import ArgumentParser
import cv2
import math
import numpy as np
import os


def closet_square(number):
    square = math.sqrt(number)
    match number:
        case 1:
            return 1
        case 2 | 3 | 4:
            return 2
        case number if square == math.floor(square):
            return number
        case _:
            return int((math.floor(square) + 1) ** 2)


def combine_videos(path_to_videos, output):
    videos_list = [name for name in os.listdir(path_to_videos)
                   if os.path.isfile(os.path.join(path_to_videos, name))]

    grid, output = None, None
    grid_size = closet_square(len(videos_list))

    videos = [video for v in videos_list if
              (video := cv2.VideoCapture(os.path.join(path_to_videos,
                                                      v))).isOpened()]

    video_params = [[video.get(i) for i in [3, 4, 5, 7]] for video in videos]

    if not video_params[:-1] == video_params[1:]:
        raise RuntimeError('Not all of the videos have the same parameters')

    width, height, frame_rate = [int(param) for param in video_params[0][:3]]
    grid = np.zeros((height * grid_size, width * grid_size, 3), dtype=np.uint8)
    output = cv2.VideoWriter(output,
                             cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                             frame_rate,
                             (grid.shape[1], grid.shape[0]))

    def insert_frame_by_frame(single_frame, output):
        while True:
            for idx, video in enumerate(single_frame):
                match video.read():
                    case True, frame:
                        cv2.putText(frame, videos_list[idx][:-4],
                                    (10, frame.shape[0] - 50),
                                    cv2.FONT_HERSHEY_PLAIN,
                                    2,
                                    (0, 255, 0),
                                    2,
                                    cv2.LINE_AA)
                        row, col = idx // grid_size, idx % grid_size
                        grid[row * height: row * height + height,
                             col * width: col * width + width,
                             :] = frame
                    case False, frame:
                        return
            output.write(grid)

    insert_frame_by_frame(videos, output)

    [video.release() for video in videos]
    output.release()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--path_to_videos', type=str, default='videos',
                        help='path to the directory contining video file')
    parser.add_argument('--output_video', type=str, default='output.avi',
                        help='path to the resulting video')
    arguments = parser.parse_args()
    combine_videos(arguments.path_to_videos, arguments.output_video)
