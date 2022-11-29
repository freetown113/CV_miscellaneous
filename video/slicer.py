from argparse import ArgumentParser
import cv2
from itertools import count
from multiprocessing import Pool, cpu_count, current_process
import os


def slice_and_save(input):
    match input:
        case path_to_video, file_name, output_path:
            video = cv2.VideoCapture(os.path.join(path_to_video, file_name))
            if not video.isOpened():
                raise RuntimeError(f'Cannot open video {path_to_video}')
            for i in count():
                match video.read():
                    case True, frame:
                        if not os.path.exists(f := os.path.join(output_path,
                                              os.path.splitext(file_name)[0])):
                            os.makedirs(f)
                        cv2.imwrite(os.path.join(f, str(i) + '.jpg'), frame)
                    case False, frame:
                        print(f'{current_process()} process wrote {i} images \
                                in {f}')
                        return
        case other:
            raise ValueError(f'Unsupported value was provided: expected \
                                  Tuple[str, str], got {type(other)}')


def slice_video(path_to_videos, output_path):
    videos_list = [(path_to_videos, name, output_path) for name in
                   os.listdir(path_to_videos)
                   if os.path.isfile(os.path.join(path_to_videos, name))]

    pool = Pool(cpu_count())
    pool.map(slice_and_save, videos_list)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--path_to_videos', type=str, default='videos',
                        help='path to the directory contining video file')
    parser.add_argument('--ouptut_path', type=str, default='output_videos',
                        help='path to the directory contining video file')
    parser.add_argument('--slicing_type', type=str, default='frames',
                        help='path to the directory contining video file')
    arguments = parser.parse_args()
    slice_video(arguments.path_to_videos, arguments.ouptut_path)
