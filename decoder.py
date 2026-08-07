from PIL import Image
import numpy as np
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import random
import secrets

seed = "8a2cea1c8415e4e95e9adb799926a88c6717903b2246c8bf7c623ebc5bc6e7a3"

img = Image.open("duck_test_1.PNG").convert("RGB")
width, height = img.size
img_array = np.array(img)

def get_pixel_lsb(coord):
    x, y = coord
    r, g, b = img_array[y, x]

    r_bin = format(r, '08b')
    g_bin = format(g, '08b')
    b_bin = format(b, '08b')

    if r_bin[-1] == g_bin[-1] == b_bin[-1]:
        return r_bin[-1]
    else:
        print("Error: r, g, and b values are not the same. Please run lsb_zero or lsb_one first.")

def pixel_decoder():
    """
    Takes pixel data based on the order given in pixel_list and outputs a binary
    """
    binary = ""
    pixels = [(x, y) for x in range(width) for y in range(height)]
    rng = random.Random(seed)
    rng.shuffle(pixels)
    pixel_list = pixels[:8]

    for coords in pixel_list:
        binary += get_pixel_lsb(coords)
    print(f"Decoded binary: {binary}")


pixel_decoder()