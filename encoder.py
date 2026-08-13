from PIL import Image
from PIL.PngImagePlugin import PngInfo
import numpy as np
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import random
import secrets

# Cryptography 
key = 'zFS1N0HR+uv7yaEMHHYwhQo+oSk4AHcZVUt4vY6oEHU='
# key = base64.b64encode(os.urandom(32)) to generate
aesgcm = AESGCM(base64.b64decode(key))
iv = os.urandom(12)
# ---------------

# Opening image
img = Image.open("duck.png").convert("RGB")
width, height = img.size
total_pixels = width * height
img_array = np.array(img)

# Reading text file
with open('text.txt', 'r', encoding="utf-8") as file:
    text = file.read()   

MESSAGE = text


def lsb_modify(coord, bit):
    """
    Modifies the least-significant-bit of a given pixel to 1 or 0.

    @param coord: Coordinates of pixel (x, y, z) to be modified. x and y are spatial coordinates, while
    z is the identifier for the colors red green blue. z can either be 0 (red), 1 (green), or 2 (blue)

    @param bit: 1 or 0. The desired output of the least significant bit.
    @return: Nothing. Only modifies the pixels of uploaded image.
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
    Encodes plaintext using AES.

    @param msg: (str) message to be encoded. 
    @return: (bytes) encoded ciphertext
    """
    plaintext = msg.encode('utf-8')
    ciphertext = aesgcm.encrypt(iv, plaintext, None)

    return ciphertext


def decoder(cipher):
    """
    Decodes ciphertext using AES. 

    @param cipher: (bytes) ciphertext created from encoder function
    @return: (str) decoded plaintext.
    """
    msg = aesgcm.decrypt(iv, cipher, None)
    plaintext = msg.decode('utf-8')

    return plaintext


def binary(ciphertext):
    """
    Converts ciphertext (bytes) into binary for lsb_modify

    @param cipher: (bytes) 
    @return: (bytes) in binary
    """
    bin = ''.join(format(byte, '08b') for byte in ciphertext)

    global binary_length
    binary_length = len(bin)

    return bin


def undo_binary(binary):
    """
    Undoes the binary function. Converts binary back into raw bytes.

    @param binary: (bytes) binary
    @return: (bytes)
    """
    result = []

    for i in range(0, len(binary), 8):
        result.append(int(binary[i:i+8], 2))

    return bytes(result)


def random_pixel(n):
    """
    Generates n unique random pixel coordinate(s)

    @param n: (int) 
    @return: (list) a list of n coordinates
    """
    pixels = [(x, y, z) for x in range(width - 1) for y in range(height - 1) for z in range(3)]

    seed = secrets.token_hex(20) # length 40
    ivh = iv.hex() # length 24
    rng = random.Random(seed)
    leng = len(binary(encoder(MESSAGE)))
    global gseed
    gseed = seed + ivh + str(leng)

    rng.shuffle(pixels)
    print(f"Your seed is: {gseed}") 
    return pixels[:n]


def hide_pixel():
    """
    Runs lsb_modify a certain amount of times.

    @return: nothing
    """
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
    """
    Returns the least-significant bit of a color of a specified pixel.

    @param coord: coordinates (x, y, z) of the pixel
    @return: (str) the lsb of the color specified by z
    """
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
    

# Testing functions
def testing_get_pixel_lsb(coord):
    """
    Returns individual pixel data. For testing purposes. Unlike get_pixel_lsb, this returns nothing.
    
    @param coord: coordinates (x, y, z) of the pixel
    @return: a print statement
    """
    x, y, _ = coord
    r, g, b = img_array[y, x]

    r_bin = format(r, '08b')
    g_bin = format(g, '08b')
    b_bin = format(b, '08b')

    print( f"Random pixel RGB: {(r_bin[-1], g_bin[-1], b_bin[-1])}" )


def pixel_decoder():
    """
    Takes pixel data based on the order given in pixel_list and outputs a binary

    @return: (str) a long string of binaries
    """
    binary = ""
    for coords in pixel_list:
        binary += get_pixel_lsb(coords)
    return binary


def aesgcm_decrypt():
    """
    Decrypts the binary message from pixel_decoder.
    
    @return: (str) the initial encoded message
    """
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

metadata = PngInfo()
metadata.add_text("tEXt", gseed)

encoded_img = Image.fromarray(img_array.astype('uint8'))

print(f"Total pixels: {total_pixels}")
print(f"Number of pixels modified: {binary_length}")
print(f"Percentage of pixels used: {(binary_length / total_pixels):.2%}")

# encoded_img.show()
encoded_img.save("duck_exported.png", pnginfo=metadata)



