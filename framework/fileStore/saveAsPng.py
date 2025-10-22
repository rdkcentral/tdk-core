#!/usr/bin/python
##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2024 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
from PIL import Image
import sys
import numpy as np

##################################################
#
# Method to decode the base64 encoded string
#
##################################################
def base64_decode(encoded):
    base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
    base64_char_to_val = {ch: idx for idx, ch in enumerate(base64_chars)}
    decoded_bytes = []
    i = 0
    while i < len(encoded):
        if encoded[i] == '=':
            break
        # Decode each block of 4 characters into 3 bytes
        b1 = base64_char_to_val.get(encoded[i], 0)
        b2 = base64_char_to_val.get(encoded[i + 1], 0)
        b3 = base64_char_to_val.get(encoded[i + 2], 0) if encoded[i + 2] != '=' else 0
        b4 = base64_char_to_val.get(encoded[i + 3], 0) if encoded[i + 3] != '=' else 0
        # Convert the 4x 6-bit numbers into 3x 8-bit bytes
        decoded_bytes.append((b1 << 2) | (b2 >> 4))
        if encoded[i + 2] != '=':
            decoded_bytes.append(((b2 & 0x0F) << 4) | (b3 >> 2))
            if encoded[i + 3] != '=':
                decoded_bytes.append(((b3 & 0x03) << 6) | b4)
        i += 4
    return bytes(decoded_bytes)

######################################################
#
# Method to write base64 decoded data into png file
#
#  filename : png file path
#  data     : base64 decoded data
#  width    : width of the image to be written (1080)
#  height   : height of the image to be written (1920)
######################################################
def write_png_file(filename, data, width, height):
    image = Image.frombytes('RGBA', (width, height), data)
    # Flip the image vertically as glreadPixels reads data in reverse order
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image.save(filename)

######################################################
#
# Method to check if image is just black
#
#  image_path : png file path
######################################################
def is_image_black(image_path):
    # Open the image
    img = Image.open(image_path)
    # Get the dimensions of the image
    width, height = img.size
    # Iterate through each pixel and check if it's black
    for x in range(width):
        for y in range(height):
            # Get the RGB values of the pixel
            r, g, b, _ = img.getpixel((x, y))
            # If any of the RGB values are not zero, the image is not completely black
            if r != 0 or g != 0 or b != 0:
                return False
    # If all pixels are black, return True
    return True

######################################################
#
# Method to write base64 decoded data into png file
#
#  file_path : file containing base64 encoded data
#  data      : base64 decoded data
#  width     : width of the image to be written (1080)
#  height    : height of the image to be written (1920)
######################################################
def decodeAndSave(file_path,width,height,png_path):
    print("File to be decoded : ",file_path)
    print("Obtained width = %d, height = %d" %(width,height));
    try:
        with open(file_path, 'r') as file:
            encoded = file.read().replace('\n', '')
    except Exception as e:
        print(f"Error: Failed to open file: {file_path}")
        print(e)
        return 1

    decoded = base64_decode(encoded)

    write_png_file(png_path, decoded, width, height)
    print(f"PNG image successfully created: {png_path}")
    if (is_image_black(png_path)):
        print("\nImage is a black screen")
        return False
    else:
        return True

def decodeAndSaveDirectly(encoded,width,height,png_path):
    decoded = base64_decode(encoded)

    write_png_file(png_path, decoded, width, height)
    print(f"PNG image successfully created: {png_path}")
    if (is_image_black(png_path)):
        print("\nImage is a black screen")
        return False
    else:
        return True

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print(f"Usage: {sys.argv[0]} <file_path>")
        print("\nAdditionial configurations available")
        print("Command line arguments:\n\t2-> width of image (eg: 1920/1280/854)\n\t3-> height of image(eg: 1080/720/480)")
        print("\t4-> File path for decoded png image(eg:output.png)")
        print("\nSample Command ---> \"python k.py encoded_image.txt 1920 1080 output.png\"")
        exit(0)
    file_path = sys.argv[1]

    if len(sys.argv) <= 3:
        print("\nWidth and height is not given , assuming 1920x1080");
        # Assuming the decoded data represents an RGBA image with a specific width and height
        width = 1920
        height = 1080
    else:
        width = int(sys.argv[2])
        height = int(sys.argv[3])

    # Write the decoded binary data to a PNG file
    if len(sys.argv) <= 5:
        png_path = sys.argv[4]
    else:
        png_path = "output.png"

    decodeAndSave(file_path,width,height,png_path)
