from PIL import Image
import numpy as np
import math
import hashlib
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import random

# Cryptography 
key = 'zFS1N0HR+uv7yaEMHHYwhQo+oSk4AHcZVUt4vY6oEHU='
aesgcm = AESGCM(base64.b64decode(key))
iv = os.urandom(12)
MESSAGE = 'insert message to be hidden here'
# ---------------

img = Image.open("duck.png").convert("RGB")
width, height = img.size
img_array = np.array(img)


def lsb_to_one(coord):
    """
    Changes a pixel's least significant bit to 1 given its x and y coordinate. Note that numpy uses (y, x) and not (x, y).
    Function uses (x, y) as input for familiarity. 
    """
    x, y = coord
    r, g, b = img_array[y, x]

    r_new = (r & 254) | 1
    g_new = (g & 254) | 1
    b_new = (b & 254) | 1

    # print(f"Coordinate {x, y} changed to one")
    img_array[y, x] = [r_new, g_new, b_new]


def lsb_to_zero(coord):
    """
    Changes a pixel's least significant bit to 0 given its x and y coordinate. Note that numpy uses (y, x) and not (x, y).
    Function uses (x, y) as input for familiarity. 
    """
    x, y = coord
    r, g, b = img_array[y, x]

    r_new = (r & 254) | 0
    g_new = (g & 254) | 0
    b_new = (b & 254) | 0

    # print(f"Coordinate {x, y} changed to zero")
    img_array[y, x] = [r_new, g_new, b_new]


def encoder(msg):
    """
    Encodes plaintext using AES
    """
    plaintext = msg.encode('utf-8')
    ciphertext = aesgcm.encrypt(iv, plaintext, None)

    return ciphertext


def binary(ciphertext):
    """
    Converts encoder into binary, more suitable for steganography
    """
    bin = ''.join(format(byte, '08b') for byte in ciphertext)

    return bin


def decoder(cipher):
    """
    Decodes ciphertext using AES
    """
    msg = aesgcm.decrypt(iv, cipher, None)
    plaintext = msg.decode('utf-8')

    return plaintext


def random_pixel(n):
    """
    Generates n unique random pixel coordinate(s)
    """
    pixel_list = set()

    while len(pixel_list) < n:
        y = random.randint(0, height - 1)
        x = random.randint(0, width - 1)

        pixel_list.add((x, y))

    # print(list(pixel_list))
    return list(pixel_list)


def binary_to_method(binary, coord):
    """
    Takes a binary as input and outputs a corresponding function order. For instance, 0011 calls
    lsb_to_zero, lsb_to_zero, lsb_to_one, lsb_to_one.
    """
    for digits in binary:
        if digits == "0":
            lsb_to_zero(coord)
        elif digits == "1":
            lsb_to_one(coord)
        else:
            print("Error: binary contains values that are not 1 or 0")


def hide_pixel(binary):
    # to_be_encoded = binary(encoder(MESSAGE))
    # pixel_list = random_pixel(len(to_be_encoded))
    to_be_encoded = binary
    pixel_list = random_pixel(len(to_be_encoded)) # generates n random pixels to hide to_be_encoded in
    # pixel_list serves also as a key for decoding as it gives the order of binaries to be read

    get_pixel_lsb(pixel_list[0])
    get_pixel_lsb(pixel_list[1])
    for bin, pixels in zip(binary, pixel_list):
        if bin == "1":
            lsb_to_one(pixels)
        elif bin == "0":
            lsb_to_zero(pixels)
        else:
            print("Error: binary contains values that are not 1 or 0")

    return pixel_list

# Testing methods
def get_pixel_lsb(coord):
    x, y = coord
    r, g, b = img_array[y, x]

    r_bin = format(r, '08b')
    g_bin = format(g, '08b')
    b_bin = format(b, '08b')

    print( f"Random pixel RGB: {(r_bin[-1], g_bin[-1], b_bin[-1])}" )
# ---------------

# rndm = random_pixel(2)
# print(f"Random pixels: {rndm}")
# get_pixel_lsb(rndm[0])
# print("POST TEST")
# get_pixel_lsb(rndm[0])

hide_pixel("10")


# print(f"Width: {width}, height: {height}")

# Image output
# encoded_img = Image.fromarray(img_array.astype('uint8'))
# encoded_img.show()
