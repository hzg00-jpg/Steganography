# Steganography

## Using
This program runs entirely on python. 

### Encoding
To use, upload an image and enter the image name in line 18 of `encoder.py`. You may want to generate a new key (line 11) with instructions on how to do so in line 12.

Then, run `encoder.py`, and the image is automatically saved in the same directory that contains `encoder.py`. The code will output a seed, which you can either save now, or extract it from the image metadata (see Exiftool viewing).

### Decoding
To decode, make sure that the image exported by `encoder.py` is in the same directory as `decoder.py` (it is by default). Input the encoder seed (line 13). Make sure that the key (line 8) is the same as the key used in `encoder.py`. Then, run the python file to execute.

## Exiftool viewing:

Run:

`C:\exiftool\exiftool.exe "C:\Users\You\Downloads\Steganography\duck_exported.png"`, making sure to change `You.` The metadata is listed next to `TE Xt`.
