 

 # This directory contains two scripts:

***split.py***:

> takes an image as input and cuts it into separate images of equal size while it is possible. The size of the desirable piece size is provided as arguments (_width_, _height_). If an image can't be divided in equal chunks, it'll be divided in equal chunks as far as possible; the rest chunk rest at the size as they are. All information about input image's sizes, chunk sizes, number of chunks is coded into each individual result image name.

**Arguments:**

- image: str - path to the image

- height: int - image height

- width: int - image width

- x_shift: int - number of pixels in horizontal (right) direction to move before start splitting an image into pieces

- y_shift: int - number of pixels in vertical (down) direction to move before start splitting an image into pieces

- output: str - path to directory where separate images will be stored



***merge.py***:

> takes a path to a directory with images (chunks of the original image) and restores the original image based on information coded into each image name.

**Arguments:**

- input_path: str - path to directory where separate images are located

- output: str - path to and name of the file where restored image will be saves

- original_img_path: str - path to the original image. It is necessary to compare if the original and the restored images have exactly the same pixels.
