from argparse import ArgumentParser
import numpy as np
import os
from PIL import Image

### ERROR handling and undefined input handling
### EXCEPTIONS right handling behaviour
### add logic to use shifts
 
class Slicer:
    def __init__(self,
                 image_path: str,
                 height: int,
                 width: int,
                 x_shift: int,
                 y_shift: int,
                 output_path: str
                 ) -> None:
        self.image = self.__open_image(image_path)
        self.height = self.__check_values(height, 'height')
        self.width = self.__check_values(width, 'width')
        self.cols = self.__check_values(x_shift, 'x_shift')
        self.rows = self.__check_values(y_shift, 'y_shift')
        self.out_path = self.__check_dir(output_path)

    def __check_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        return path

    def __open_image(self,
                     image_path: str
                     ) -> np.array:
        return np.array(Image.open(image_path))

    def __check_values(self, arg, name):
        if not isinstance(arg, int):
            raise ValueError(f'Provide {name} argument as an int, you \
                               provided argument of type {type(arg)}')
        h, w = self.image.shape[:2]
        if name == 'height' and arg > h or name == 'width' and arg > w:
            raise ValueError(f'Patch size cannot be more than image size \
                               by any dimension. You provided patch height: \
                               {self.height} and width: {self.width}, \
                               while image height: {h} and width: {w}')
        if (name == 'height' or name == 'width') and arg <= 0:
            raise ValueError(f'Patch size cannot be less than 1 by any \
                               dimension. You provided {arg} value for \
                               {name} argument.')
        if (name == 'x_shift' or name == 'y_shift') and arg < 0:
            raise ValueError(f'The shift cannot be negative by any \
                               dimension. You provided {arg} value for \
                               {name} argument.')
        else:
            return arg

    def slice(self):
        height, width = self.image.shape[:2]
        row_spare, col_spare = height % self.height, width % self.width

        v_chunks = self.split_reminder(self.image, self.width, axis=1) \
            if row_spare else self.split_evenly(self.image, self.width,
                                                axis=0)

        for v_idx, chank in enumerate(v_chunks):
            h_chunks = self.split_reminder(chank, self.height, axis=0) \
                if col_spare else self.split_evenly(self.image, self.height,
                                                    axis=1)
            for h_idx, img in enumerate(h_chunks):
                self.save_image(img, h_idx, v_idx, self.height, self.width,
                                width, height)

    def split_evenly(self,
                     array: np.array,
                     chunk_size: int,
                     axis: int = 0
                     ) -> np.array:
        return np.array_split(array, np.ceil(array.shape[axis] / chunk_size),
                              axis=axis)

    def split_reminder(self,
                       array: np.array,
                       chunk_size: int,
                       axis: int = 0
                       ) -> np.array:
        indices = np.arange(chunk_size, array.shape[axis], chunk_size)
        return np.array_split(array, indices, axis)

    def save_image(self,
                   array: np.array,
                   col: int,
                   row: int,
                   patch_w: int,
                   patch_h: int,
                   img_w: int,
                   img_h: int
                   ) -> None:
        Image.fromarray(array).save(os.path.join(self.out_path, str(col) + '_'
                                                 + str(row) + '_' +
                                                 str(patch_w) + '_' +
                                                 str(patch_h) + '_' +
                                                 str(img_w) + '_' + str(img_h)
                                                 + '_image.png'), 'PNG')


def main(args):
    slicer = Slicer(args.image, args.height, args.width, args.x_shift,
                    args.y_shift, args.output)
    slicer.slice()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--image', help='path to image',
                        default='Cape_Town.jpg', type=str)
    parser.add_argument('--height', help='height of a patch',
                        default=300, type=int)
    parser.add_argument('--width', help='width of a patch',
                        default=300, type=int)
    parser.add_argument('--x_shift', help='shift by x coodinate',
                        default=0, type=int)
    parser.add_argument('--y_shift', help='shift by y coodinate',
                        default=0, type=int)
    parser.add_argument('--output', help='result images directory',
                        default='split_output', type=str)
    arguments = parser.parse_args()
    main(arguments)
