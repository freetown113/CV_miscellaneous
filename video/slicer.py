from argparse import ArgumentParser
import cv2
from itertools import count, repeat
from multiprocessing import Pool, cpu_count, current_process
import os


def slice_and_save(input: str,
                   slicing_type: str
                   ) -> None:
    '''Principal function that gets one video and save all frames or
    frame per second in the corresponding folder'''
    match input:
        case path_to_video, file_name, output_path:
            video = cv2.VideoCapture(os.path.join(path_to_video, file_name))
            if not video.isOpened():
                raise RuntimeError(f'Cannot open video {path_to_video}')
            frame_rate = video.get(5)
            for i in count():
                match video.read():
                    case True, frame:
                        if not os.path.exists(f := os.path.join(output_path,
                                              os.path.splitext(file_name)[0])):
                            os.makedirs(f)
                        if slicing_type == 'seconds' and i % frame_rate == 0:
                            cv2.imwrite(os.path.join(f, str(i) + '.jpg'),
                                        frame)
                        elif slicing_type == 'frames':
                            cv2.imwrite(os.path.join(f, str(i) + '.jpg'),
                                        frame)
                        else:
                            pass
                    case False, frame:
                        print(f'{current_process()} process wrote {i} images \
                                in {f}')
                        return
        case other:
            raise ValueError(f'Unsupported value was provided: expected \
                                  Tuple[str, str], got {type(other)}')


def slice_video(path_to_videos: str,
                output_path: str,
                num_process: int,
                slicing_type: str
                ) -> None:
    '''Main function: Gets a path to the folder containing videos.
    Makes a list of all the files in the folder and launchs principal 
    function in the number of processes provided by user'''
    videos_list = [(path_to_videos, name, output_path) for name in
                   os.listdir(path_to_videos)
                   if os.path.isfile(os.path.join(path_to_videos, name))]

    match num_process:
        case None:
            process = cpu_count()
        case other:
            process = other

    pool = Pool(process)
    pool.starmap(slice_and_save, zip(videos_list, repeat(slicing_type)))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--path_to_videos', type=str, default='videos',
                        help='path to the directory contining video file')
    parser.add_argument('--ouptut_path', type=str, default='output_videos',
                        help='path to the directory contining video file')
    parser.add_argument('--slicing_type', type=str, default='seconds',
                        choices=['frames', 'seconds'],
                        help='path to the directory contining video file')
    parser.add_argument('--num_process', type=str, default=None,
                        help='number of process to run for handling data')
    arguments = parser.parse_args()
    slice_video(arguments.path_to_videos, arguments.ouptut_path,
                arguments.num_process, arguments.slicing_type)
