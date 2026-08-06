import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM 
import base64  

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

test1 = encode("the quick black fox jumped over the lazy god")
print(iv)
decode(test1)

