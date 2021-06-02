
# third-party Libs
import PIL as pil
from PIL import Image

# built-in Libs
import os
from datetime import datetime
import sys

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
def main():
    
    try:
        if sys.argv[1] == ("hide"):
            image = str(sys.argv[2])
            payload = str(sys.argv[3])
            with open(payload, "r") as file:
                payload = file.read()
            save_loc = str(sys.argv[4])
            left_over = hide(image, payload, save_loc)
            
        else:
            image = str(sys.argv[2])
            result = show(image)
            print(result)
        print("\ndone")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
