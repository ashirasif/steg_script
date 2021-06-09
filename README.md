# Steganography Script 
A python script coded to perform LSB steganography. This script only accepts **.png** since they use loseless compression. 

# Arguments
* --action, -a : action to perform. Either "encode" or "decode".
* --image, -i : location of image to encode or decode th payload
* --payload, -p : payload to encode. pass --file then payload will be considered as location to text file to be used as payload
* --fromfile : if passed with action=encode, the payload string will be considered as location to text file.
*  --tofile : only when action = decode, this argument will be the location of (.txt) file to write the output from image
* --dest DEST, -d DEST  destination for the image (with name + ext)
* --help, -h : for help

# Example

## Encode
To save some text in an image, set action to *encode* using **-a** flag, pass **-i** with *location/of/image.png*, use **-p** for payload, and **-d** flag for location where you want to save the image.  

```$ python3 steg.py -a encode -i "location/of/image/to/use.png" -p "this text will be saved" -d "location/to/save/text/containing/image.png"```  

To use text from a .txt file, pass **--fromfile** flag. This will assume that **-p** contains the location of the text file.

```$ python3 steg.py -a encode -i "location/of/image/to/use.png" --fromfile -p "location/of/textfile.txt -d "location/to/save/text/containing/image.png"```

## Decode
To see what is saved inside the an image (or "decode" the text), set **-a** (action) to **decode**, tell which image to decode text from by using **-i** flag with **location/of/image.png**.  

 ```$ python3 steg.py -a decode -i "location/of/image/to/decode.png```

by default, the text obtained from the image will be printed on the screen. However, if you want the text to be saved in a text file (.txt), then pass the flag **--tofile**.  

```$ python3 steg.py -a decode --tofile -i location/of/image.png```

## Help
run with **-h** flag or **--help** for help

# What's left to do?
There is no feature to set a password and encrypt the text in image. That is still left to do.