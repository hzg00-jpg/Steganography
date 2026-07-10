from PIL import Image
import numpy as np
import math

img = Image.open("duck.png").convert("RGB")

width, height = img.size
img_array = np.array(img)

def numb_to_coordinate(pixel_num):
    """
    Converts a pixel number into x and y coordinates. Counting starts at 0, from left to right
    then down. 0 refers to (0,0) coordinate.
    """
    row = math.floor(pixel_num / width)
    col = pixel_num % width

    return [row, col]

def lsb_to_one(x, y):
    """
    Changes a pixel's least significant bit to 1 given its x and y coordinate. Note that numpy uses (y, x) and not (x, y).
    Function uses (x, y) as input for familiarity. 
    """
    r, g, b = img_array[y, x]

    r_new = (r & 254) | 1
    g_new = (g & 254) | 1
    b_new = (b & 254) | 1

    img_array[y, x] = [r_new, g_new, b_new]


def lsb_to_zero(x, y):
    """
    Changes a pixel's least significant bit to 0 given its x and y coordinate. Note that numpy uses (y, x) and not (x, y).
    Function uses (x, y) as input for familiarity. 
    """
    r, g, b = img_array[y, x]

    r_new = (r & 254) | 0
    g_new = (g & 254) | 0
    b_new = (b & 254) | 0

    img_array[y, x] = [r_new, g_new, b_new]

print(f"Width: {width}, height: {height}")
lsb_to_one(1000, 100)

# Image output
encoded_img = Image.fromarray(img_array.astype('uint8'))
encoded_img.show()