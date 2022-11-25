from argparse import ArgumentParser
import numpy as np
from PIL import Image
from typing import Tuple

### ERROR handling and undefined input handling
### EXCEPTIONS right handling behaviour
 
class Slicer:
    def __init__(self,
                 image_path: str,
                 height: int,
                 width: int,
                 x_shift: int,
                 y_shift: int
                 ) -> None:
        self.height = height
        self.width = width
        self.cols = x_shift
        self.rows = y_shift
        self.image = self.__open_image(image_path)

    def __open_image(self,
                     image_path: str
                     ) -> np.array:
        return np.array(Image.open(image_path))

    def get_patch_sizes(self) -> Tuple[int, int, int, int]:
        h, w, c = self.image.shape
        return (*divmod(h, self.height), *divmod(w, self.width))

    def slice(self):
        rows, row_spare, cols, col_spare = self.get_patch_sizes()

        v_chunks = self.split_reminder(self.image, self.height, axis=0) \
            if row_spare else self.split_evenly(self.image, self.height,
                                                axis=0)

        for v_idx, chank in enumerate(v_chunks):
            h_chunks = self.split_reminder(chank, self.width, axis=1) \
                if col_spare else self.split_evenly(self.image, self.width,
                                                    axis=1)
            for h_idx, img in enumerate(h_chunks):
                Image.fromarray(img).save('output/' + str(v_idx) + '_' +
                                          str(h_idx) + '_image.png')

    def split_evenly(self, array, chunk_size, axis=0):
        return np.array_split(array, np.ceil(array.shape[axis] / chunk_size),
                              axis=axis)

    def split_reminder(self, array, chunk_size, axis=0):
        indices = np.arange(chunk_size, array.shape[axis], chunk_size)
        return np.array_split(array, indices, axis)


def main(args):
    slicer = Slicer(args.image, args.height, args.width, args.x_shift,
                    args.y_shift)
    slicer.slice()


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--image', help='path to image',
                        default='image.png')
    parser.add_argument('--height', help='height of a patch',
                        default=300, type=int)
    parser.add_argument('--width', help='width of a patch',
                        default=300, type=int)
    parser.add_argument('--x_shift', help='shift by x coodinate',
                        default=0, type=int)
    parser.add_argument('--y_shift', help='shift by y coodinate',
                        default=0, type=int)
    arguments = parser.parse_args()
    main(arguments)
