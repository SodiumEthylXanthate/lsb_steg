# Imports
from PIL import Image
import numpy as np
import re
from os import path

# Constants
CHANNELS = 3  # Number of channels in RGB mode to properly convert from array to image
START    = "[START]"
END      = "[END]"
PATTERN  = re.compile(r"\[START\](?P<msg>.+)\[END\]")


def load_img(img_path):
    """
    In:  img_path, str
    Out: img_bytes, list of strings
         img_height, int
         img_width, int
         False if invalid path
    """
    # Validate existence of image path
    if not path.exists(img_path):
        raise Exception("The path you have entered does not exist")

    img = Image.open(img_path)
    pixels = list(img.getdata().convert('RGB'))
    flattened_px = [px for tup in pixels for px in tup]
    img_bytes = [format(px, '08b') for px in flattened_px]  # List containing individual bytes of the image as strings
    img_height, img_width = img.size[0], img.size[1]

    return img_bytes, img_height, img_width


def lsb_encode(img_bytes, msg, height, width):
    """
    In:  img_bytes, list of strings
         msg, string
         height, int
         width, int
    Out: encoded_img, PIL image object (if successful)
         False                         (if unsuccessful)
    """
    padded_msg = f"{START}{msg}{END}"
    #DEBUG###print(padded_msg)
    msg_bits = ''.join([format(ord(letter), '08b') for letter in padded_msg])  # String containing all message bits

    # Safeguard to not allow messages longer than what the image can contain
    if len(msg_bits) > len(img_bytes):
        return False

    # Encoding message in image bytes
    for byte, bit, index in zip(img_bytes, msg_bits, range(0, len(msg_bits) - 1)):  # Changes the actual initial list of image bytes as needed
        img_bytes[index] = img_bytes[index][:-1] + bit  # Changes last bit of each byte to corresponding message bit
    
    # Converting back to image object
    num_array = [int(byte, 2) for byte in img_bytes]  # Base 10 numbers instead of bytes to prevent converting from 2D array
    encoded_array = [num_array[i:i+3] for i in range(0, len(num_array), 3)]  # 2D array that can be converted back into an image
    numpy_encoded = np.asarray(encoded_array, dtype=np.uint8).reshape(width, height, CHANNELS)  # Array converted to numpy to work with PIL
    encoded_img = Image.fromarray(numpy_encoded, mode="RGB")
    
    return encoded_img
    

def lsb_decode(img_bytes):
    """
    In:  img_bytes, list of strings
    Out: message, str (if successful)
         False        (if unsuccessful)
    """
    img_lsb = ''.join([byte[-1] for byte in img_bytes])  # String of last bits of all bytes in the image
    lsb_bytes = [img_lsb[i:i+8] for i in range(0, len(img_lsb), 8)]  # 8 bit strings
    extracted_text = ''.join([chr(int(byte, 2)) for byte in lsb_bytes])  # String of all text converted from the extracted bytes
    #DEBUG###print(extracted_text)
    match = PATTERN.search(extracted_text)

    # Safegueard to not throw an error if no message was found
    if match:
        message = match.group('msg')  # Return the extracted message
        return message
    else:
        return False


def main():
    help(load_img)
    help(lsb_encode)
    help(lsb_decode)


if __name__ == "__main__":
    main()





# TODO:
# bug where in long messages the last ] in padding gets translated to \
# main loop --> split in three seperate apps
# add argparse?
# make gui version?
# add noise to rest of the image so not only the bytes containing the message are changed
# idea for noise? only change bytes in certain intervals, like every img_len // msg_len bytes
# would produce a key in encoding and ask for it in decoding
# maybe embed the key in the beginning of the message (always reserve a certain amount of bits for that)
# add a check to make sure the message bit amount is shorter than image bytes amount
# make it an option to encrypt the message before hiding it in the image
# add a way to detect if an extracted message is encrypted and using which cipher + a way to decrypt said message
