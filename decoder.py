from PIL import Image
import numpy as np
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import base64
import random
import secrets

# Cryptography 
key = 'zFS1N0HR+uv7yaEMHHYwhQo+oSk4AHcZVUt4vY6oEHU='
aesgcm = AESGCM(base64.b64decode(key))
# --------------------------------------------------

ENCODER_SEED = "1e76b1d3c935751f4ad8585d4a7b489d0ed40872744639b6b60abdf07748b799200"

img = Image.open("tmp_la2hw4v.PNG").convert("RGB")

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


def binary(ciphertext):
    """
    Converts encoder into binary
    """
    bin = ''.join(format(byte, '08b') for byte in ciphertext)

    return bin


def pixel_decoder():
    binary = ""

    pixels = [(x, y) for x in range(width - 1) for y in range(height - 1)]
    seed = from_seed()
    msg_length = from_seed("length")

    rng = random.Random(seed)
    rng.shuffle(pixels)
    pixel_list = pixels[:msg_length]

    for coords in pixel_list:
        # testing_get_pixel_lsb(coords)
        binary += get_pixel_lsb(coords)
    return binary


def from_seed(param = "seed"):
    seed = ENCODER_SEED[:40]
    iv = ENCODER_SEED[40:64]
    length = ENCODER_SEED[64:]

    if param == "seed":
        return seed
    elif param == "iv":
        return iv
    elif param == "length" or "len":
        return int(length)


def undo_binary(bin):
    return bytes(
        int(bin[i:i+8], 2)
        for i in range(0, len(bin), 8)
    )

def aesgcm_decrypt():
    returned_binary = pixel_decoder()
    un_binary = undo_binary(returned_binary)
    iv_as_bytes = bytes.fromhex(from_seed("iv"))
    plaintext = aesgcm.decrypt(iv_as_bytes, un_binary, None)
    print(plaintext.decode("utf-8"))


# Testing methods
def testing_get_pixel_lsb(coord):
    x, y = coord
    r, g, b = img_array[y, x]

    r_bin = format(r, '08b')
    g_bin = format(g, '08b')
    b_bin = format(b, '08b')

    print( f"Random pixel RGB: {(r_bin[-1], g_bin[-1], b_bin[-1])}" )
# ---------------

aesgcm_decrypt()

