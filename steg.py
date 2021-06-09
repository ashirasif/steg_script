
# third-party Libs
from genericpath import exists
import PIL as pil
from PIL import Image

# built-in Libs
import os
from datetime import datetime
import argparse
import sys

# command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--action", "-a", help="which action to perform. actions are either 'encode' or 'decode'")
parser.add_argument("--image", "-i", help="address of image to save text of extract text from (depending on action)")
parser.add_argument("--payload", "-p", help="payload to save")
parser.add_argument("--destination", "-d", help="destination address for saving the manipulated image")
parser.add_argument("--tofile", "-f", help="address of text file to which, the extracted text will be written. Only pass it when action=decode, else the program will exit")
parser.add_argument("--fromfile", action="store_true" ,help="if passed, the payload will be used as address of text file from which text will be read and saved to an image. Only pass when action=encode.")
args = parser.parse_args()

# function for binary conversion (8-bit)
def binary(num):
    result = ""
    while num > 0:
        a = num % 2
        num = num // 2
        result += str(a)
    if len(result) < 8:
        result += "0" * (8 - len(result))
    result = result[::-1]
    return result

# function for binary conversion (16-bit)
def binary16(num):
    result = ""
    while num > 0:
        a = num % 2
        num = num // 2
        result += str(a)
    if len(result) < 16:
        result += "0" * (16 - len(result))
    result = result[::-1]
    return result

# turn payload into binary form
def Payload(payload):
    result = ""
    result += binary16(len(payload))
    for i in range(0, len(payload)):
        a = ord(payload[i])
        result += str(binary(a))
    return result

# hides the payload in image using LSB steganography
def hide(image, payload, dest):
    destination = str(dest)
    i = 0
    left_over = ""
    with Image.open(image).convert("RGBA") as img:
        width, height = img.size

        if len(payload) * 8 > width * height:
            payload = Payload(payload[:(width*height)])
            left_over = Payload(payload[(width * height):])
        else:
            payload = Payload(payload)

        for x in range(0, width):
            for y in range(0, height):
                pixel = list(img.getpixel((x, y)))
                for n in range(0, 4):
                    if i < len(payload):
                        pixel[n] = pixel[n] & ~1 | int(payload[i])
                        i += 1
                img.putpixel((x, y), tuple(pixel))
        img.save(str(destination), "PNG")

        return left_over


# convert to decimal
def decimal16(msg):
    result = 0
    msg = msg[::-1]
    for i in range(0, len(msg)):
        if msg[i] == ("1"):
            result += 2 ** int(i)
    return int(result)

# extract payload from image
def show(image):
    length = 0
    result = ""
    x = 0
    with Image.open(image) as img:
        width, height = img.size
        for y in range(0, 4):
            pixel = list(img.getpixel((x, y)))
            for n in range(0, len(pixel)):
                result = result + str(pixel[n] & 1)
        pixel.clear()

        length = decimal16(result)
        print(length)
        result = ""

        for x in range(0, width):
            for y in range(0, height):
                pixel = list(img.getpixel((x, y)))
                for n in range(0, len(pixel)):
                    if len(result) == 16 + (length * 8):
                        a = decode(result)
                        return a
                    pixel[n] = pixel[n] & 1
                    result = result + str(pixel[n])

# decode the extracted payload
def decode(msg):
    msg = msg[16:]
    result = ""
    array = []
    a = 0
    for i in range(8, len(msg), 8):
        array.append(msg[a:i])
        a = i
    array.append(msg[a:])

    a = 0
    for i in array:
        i = i[::-1]
        for e in range(0, len(i)):
            if i[e] == ("1"):
                a += 2 ** e
        result = result + str(chr(a))
        a = 0

    return result

# main function 
# args = command line arguments
def main(args):
    try:
        # taking care of command line arguments and declaring needed variables
        if args.action is not None:
            if args.action == 'encode' or args.action == "decode":
                action = args.action
            else:
                sys.exit("{} is not a valid action. Run with -h for more info.")
        else:
            sys.exit("No action defined, use --action or -a to define the action. For more info run with -h.")

        if action == "encode":
            # if action==encode, make sure image, payload, dest arguments are provided.
            if args.image is not None:
                img = args.image
                assert os.path.exists(img), "{} does not exist.".format(img)
                assert img.endwith(".png"), "Only png format is support."
            else:
                sys.exit("image is not defined. Define one with -i or --image flag. Run with -h for more info.")
            if args.payload is not None:
                if args.fromfile:
                    assert (args.payload).endswith(".txt"), "make sure you provide the location of a text file."
                    assert os.path.exists(args.payload), "{} does not exist.".format(args.payload)
                    with open(args.payload, 'r') as f:
                        payload = f.read()
                        f.close()
                else:
                    payload = args.payload
            else:
                sys.exit("No payload is passed. Define the payload with -p or --payload flag. Run with -h for more info.")
            if args.destination is not None:
                assert args.destination.endswith(".png"), "image can be only saved as png"
                dest = args.destination
            else:
                sys.exit("No address to save the image is passed, pass it with -d or --destination flag. Run with -h for more info.")
            
            # encoding payload in img
            hide(img, payload, dest)

        else: 
            # if action==decode, make sure the image is provided
            if args.image is not None:
                assert (args.image).endswith(".png"), "Only png is supported."
                assert os.path.exists(args.image), "{} does not exist.".format(args.image)
                img = args.image
            else:
                sys.exit("No image defined to extract text from. Pass with -i or --image. Run with -h for help.")
            
            # extracting text for image(img)
            result = show(img)

            # write text to file if 
            if args.tofile is not None:
                assert (args.tofile).endswith(".txt"), "file to save text should have extension '.txt'"
                with open(args.tofile, 'w') as f:
                    f.write(result)
                    print("text saved to {}".format(args.tofile))
                    f.close()
            else:
                print(result)

    except Exception as e:
        print(e)
    finally:
        print("done")

if __name__ == '__main__':
    main(args)
