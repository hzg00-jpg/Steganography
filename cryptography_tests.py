import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM 
import base64  
import random
import secrets

key = 'zFS1N0HR+uv7yaEMHHYwhQo+oSk4AHcZVUt4vY6oEHU='
aesgcm = AESGCM(base64.b64decode(key))
iv = os.urandom(12) # creates unique ciphers for identical message


def encode(msg):
    plaintext = msg.encode('utf-8')
    ciphertext = aesgcm.encrypt(iv, plaintext, None)
    # cipher_b64 = base64.b64encode(ciphertext).decode('utf-8')

    print(ciphertext)
    return ciphertext

def decode(cipher):
    msg = aesgcm.decrypt(iv, cipher, None)
    plaintext = msg.decode('utf-8')

    print(plaintext)
    return plaintext

def generate_random(n):
    pixels = [(x,y) for x in range(10) for y in range(10)]
    global seed
    seed = "7545438cfc7740d3c403fda1056c9b29dec5a3b819200c1081f36adf85137a33"
    rng = random.Random(seed)

    rng.shuffle(pixels)
    print(seed)

def recreate_order(n):
    pixels = [(x, y) for x in range(10) for y in range(10)]

    rng = random.Random(seed)
    rng.shuffle(pixels)

    print(pixels[:n])
    return pixels[:n]

# test1 = encode("the quick black fox jumped over the lazy god")
# print(iv)
# decode(test1)

generate_random(2)
recreate_order(2)

