from PIL import Image
import numpy as np
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import random

# Cryptography 
key = 'zFS1N0HR+uv7yaEMHHYwhQo+oSk4AHcZVUt4vY6oEHU='
# key = base64.b64encode(os.urandom(32)) to generate
aesgcm = AESGCM(base64.b64decode(key))
# --------------------------------------------------

ENCODER_SEED = "8bb8ed5c48ff2117654d80ca0e182f40846ef0e792893fa2ad1c07a1ced3c1cd416"

img = Image.open("duck_exported.PNG").convert("RGB")

width, height = img.size
img_array = np.array(img)

def from_seed(param = "seed"):
    """
    Extracts data from a given seed. 

    @param param: (str) the desired data type to extract. Can be seed, iv, or length/len. Defaults to seed.
    """
    try:
        seed = ENCODER_SEED[:40] # contains (x, y, z) coordinate information
        iv = ENCODER_SEED[40:64] # initialization vector used in AES
        length = ENCODER_SEED[64:]

        if param == "seed":
            return seed
        elif param == "iv":
            return iv
        elif param == "length" or "len":
            return int(length)
        
    except Exception as e:
        print(f"An error occurred: {e}")


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


def binary(ciphertext):
    """
    Converts ciphertext (bytes) into binary for lsb_modify
    
    @param cipher: (bytes) 
    @return: (bytes) in binary
    """
    bin = ''.join(format(byte, '08b') for byte in ciphertext)

    return bin


def undo_binary(binary):
    """
    Undoes the binary function. Converts binary back into raw bytes.

    @param binary: (bytes)
    @return: (bytes)
    """
    result = []

    for i in range(0, len(binary), 8):
        result.append(int(binary[i:i+8], 2))

    return bytes(result)


def pixel_decoder():
    """
    Takes seed info and extracts information from specified pixels. Outputs binary data.

    @return: (bytes) 
    """
    binary = ""

    pixels = [(x, y, z) for x in range(width - 1) for y in range(height - 1) for z in range(3)]
    seed = from_seed()
    msg_length = from_seed("length")

    rng = random.Random(seed)
    rng.shuffle(pixels)
    pixel_list = pixels[:msg_length]

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
    iv_as_bytes = bytes.fromhex(from_seed("iv"))
    plaintext = aesgcm.decrypt(iv_as_bytes, un_binary, None)
    print(plaintext.decode("utf-8"))


# Testing methods
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
# ---------------

aesgcm_decrypt()



