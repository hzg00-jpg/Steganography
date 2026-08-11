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
# ---------------

img = Image.open("duck.png").convert("RGB")
width, height = img.size
img_array = np.array(img)

with open('text.txt', 'r', encoding="utf-8") as file:
    text = file.read()   


MESSAGE = text

def lsb_modify(coord, bit):
    """
    Bit can be 0 or 1
    """
    x, y, z = coord

    r, g, b = img_array[y, x]

    if bit in (0, 1):

        if z == 0:
            r_new = (r & 254) | bit
            g_new = g
            b_new = b
        elif z == 1:
            g_new = (g & 254) | bit
            r_new = r
            b_new = b
        elif z == 2:
            b_new = (b & 254) | bit
            r_new = r
            g_new = g
        else:
            print("Error: z out of bounds. z must be either 0, 1, or 2.")
    else:
        print("Invalid bit")

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
    pixels = [(x, y, z) for x in range(width - 1) for y in range(height - 1) for z in range(3)]
    global seed

    seed = secrets.token_hex(20) # length 40
    ivh = iv.hex() # length 24
    rng = random.Random(seed)
    leng = len(binary(encoder(MESSAGE)))

    rng.shuffle(pixels)
    print(f"Your seed is: {seed}{ivh}{leng}") 
    return pixels[:n]


def hide_pixel():
    to_be_encoded = binary(encoder(MESSAGE))

    global pixel_list
    pixel_list = random_pixel(len(to_be_encoded)) # generates n random pixels to hide to_be_encoded in

    for bin, pixels in zip(to_be_encoded, pixel_list):
        if bin == "1":
            lsb_modify(pixels, 1)
        elif bin == "0":
            lsb_modify(pixels, 0)
        else:
            print("Error: binary contains values that are not 1 or 0")


def get_pixel_lsb(coord):
    x, y, z = coord
    r, g, b = img_array[y, x]

    r_bin = format(r, '08b')
    g_bin = format(g, '08b')
    b_bin = format(b, '08b')

    if z == 0:
        return r_bin[-1]
    elif z == 1:
        return g_bin[-1]
    elif z == 2: 
        return b_bin[-1]
    else:
        print("Error: z out of bounds")
    

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
    x, y, _ = coord
    r, g, b = img_array[y, x]

    r_bin = format(r, '08b')
    g_bin = format(g, '08b')
    b_bin = format(b, '08b')

    print( f"Random pixel RGB: {(r_bin[-1], g_bin[-1], b_bin[-1])}" )


def aesgcm_decrypt():
    returned_binary = pixel_decoder()
    un_binary = undo_binary(returned_binary)
    plaintext = aesgcm.decrypt(iv, un_binary, None)
    print(plaintext.decode("utf-8"))


# ------------------------------
# Testing lsb_to_x function
# ------------------------------
# rndm = random_pixel(1)
# print(f"Random pixels: {rndm}")
# testing_get_pixel_lsb(rndm[0])
# lsb_modify(rndm[0], 0)
# print("POST TEST")
# testing_get_pixel_lsb(rndm[0])


hide_pixel()

# Image output
print(f"Width: {width}, height: {height}")
encoded_img = Image.fromarray(img_array.astype('uint8'))
encoded_img.show() 

