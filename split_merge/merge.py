from argparse import ArgumentParser
import numpy as np
import os
from PIL import Image
from typing import Tuple


class Glue:
    '''This class contains all methods necessary to assemble fragmented
    parts into the whole image like it was before splitting
    '''
    def __init__(self,
                 path_to_folder: str,
                 output_path: str
                 ) -> None:
        self.path = path_to_folder
        self.out_path = output_path
        self.images = None

    def __open_image(self,
                     image_path: str
                     ) -> np.array:
        '''Opening image and convert it to numpy array'''
        return np.array(Image.open(image_path))

    def __get_image_info(self,
                         img
                         ) -> Tuple[int, int, int, int, int]:
        '''Collecting information about ofiginal image parameters and
        patches parameters based on info coded into patches names
        '''
        name, _ = os.path.splitext(img)

        patch_w, patch_h, img_w, img_h = name.split('_')[2:-1]
        patch_w, patch_h, img_w, img_h = int(patch_w), int(patch_h), \
            int(img_w), int(img_h)

        num_vertical_patches, spare_vertial = divmod(img_w, patch_w)
        num_horizontal_patches, spare_horizontal = divmod(img_h, patch_h)
        num_vertical_patches += 1 if spare_vertial else num_vertical_patches
        num_horizontal_patches += 1 if spare_horizontal else \
            num_horizontal_patches

        assert num_vertical_patches * \
            num_horizontal_patches == len(self.images)

        channels = self.__open_image(os.path.join(self.path,
                                                  img)).shape[2]

        return patch_w, patch_h, img_w, img_h, channels

    def assamble(self) -> None:
        '''Principal method that makes a list of patches containing in the
        folder and based on info about original image and patches construct
        a grid of size of ofiginal image. Then openeach patch and put it in
        corresponding cell of the grid to reconstruct the original image.
        '''
        self.images = [name for name in os.listdir(self.path)
                       if os.path.isfile(os.path.join(self.path, name))]

        patch_w, patch_h, img_w, img_h, channels = \
            self.__get_image_info(self.images[0])

        grid = np.zeros((img_h, img_w, channels), dtype=np.uint8)
        for img in self.images:
            array = self.__open_image(os.path.join(self.path, img))

            height, width = array.shape[:2]
            row, col = os.path.splitext(img)[0].split('_')[:2]
            row, col = int(row), int(col)

            grid[row * patch_h: row * patch_h + height,
                 col * patch_w: col * patch_w + width,
                 :] = array

        Image.fromarray(grid).save(self.out_path, 'PNG')


def compare_images(path_image1, path_image2):
    '''Function that conmare two images provided and retur a message
    indication if there some difference between them or not
    '''
    img1, img2 = [np.array(Image.open(path)) for path
                  in (path_image1, path_image2)]

    result = np.array_equal(img1, img2)
    match result:
        case True:
            print('Images are absolutely equal')
        case False:
            print('There are differences in images')


def main(args):
    assembler = Glue(args.input_path, args.output)
    assembler.assamble()
    compare_images(args.output, args.original_img_path)


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--input_path', help='path to directory containing \
                                              images to be merged',
                        default='split_output', type=str)
    parser.add_argument('--output', help='result images directory',
                        default='./image.png', type=str)
    parser.add_argument('--original_img_path', help='path to original image',
                        default='./Cape_Town.jpg', type=str)                 
    arguments = parser.parse_args()
    main(arguments)
