from PIL import Image
import numpy as np
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import random
import secrets

# Cryptography 
key = 'zFS1N0HR+uv7yaEMHHYwhQo+oSk4AHcZVUt4vY6oEHU='
aesgcm = AESGCM(base64.b64decode(key))
iv = os.urandom(12)
MESSAGE = 'WES????SI'
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


def decoder(cipher):
    """
    Decodes ciphertext using AES. Takes bytes as input.
    """
    msg = aesgcm.decrypt(iv, cipher, None)
    plaintext = msg.decode('utf-8')

    return plaintext


def binary(ciphertext):
    """
    Converts encoder into binary
    """
    bin = ''.join(format(byte, '08b') for byte in ciphertext)

    return bin

def undo_binary(bin):
    return bytes(
        int(bin[i:i+8], 2)
        for i in range(0, len(bin), 8)
    )


def random_pixel(n):
    """
    Generates n unique random pixel coordinate(s)
    """
    pixels = [(x, y) for x in range(width - 1) for y in range(height - 1)]
    global seed

    seed = secrets.token_hex(20) # length 40
    ivh = iv.hex() # length 24
    rng = random.Random(seed)
    leng = len(binary(encoder(MESSAGE)))

    rng.shuffle(pixels)
    print(f"Your seed is: {seed}{ivh}{leng}") 
    return pixels[:n]


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


def hide_pixel():
    to_be_encoded = binary(encoder(MESSAGE))

    global pixel_list
    pixel_list = random_pixel(len(to_be_encoded)) # generates n random pixels to hide to_be_encoded in

    for bin, pixels in zip(to_be_encoded, pixel_list):
        if bin == "1":
            lsb_to_one(pixels)
        elif bin == "0":
            lsb_to_zero(pixels)
        else:
            print("Error: binary contains values that are not 1 or 0")


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
    for coords in pixel_list:
        binary += get_pixel_lsb(coords)
    return binary


# Testing functions
def testing_get_pixel_lsb(coord):
    x, y = coord
    r, g, b = img_array[y, x]

    r_bin = format(r, '08b')
    g_bin = format(g, '08b')
    b_bin = format(b, '08b')

    print( f"Random pixel RGB: {(r_bin[-1], g_bin[-1], b_bin[-1])}" )
# ---------------

# ------------------------------
# Testing lsb_to_x function
# ------------------------------
# rndm = random_pixel(2)
# print(f"Random pixels: {rndm}")
# testing_get_pixel_lsb(rndm[0])
# lsb_to_zero(rndm[0])
# print("POST TEST")
# testing_get_pixel_lsb(rndm[0])


hide_pixel()

# Image output
print(f"Width: {width}, height: {height}")
encoded_img = Image.fromarray(img_array.astype('uint8'))
encoded_img.show()
