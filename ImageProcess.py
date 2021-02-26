from PIL import Image
import numpy
import tkinter as tk
from tkinter import filedialog

def decode_img(img, delimiter='`'):
    width,height = img.size
    data = numpy.array(img)
    raw_bits = ""

    for i in range(height):
        for j in range(width):
            r,g,b,*_ = map(lambda x: format(x, "08b"), data[i][j])
            raw_bits += r[-1] + g[-1] + b[-1]
    
    raw_bytes = [raw_bits[i:i+8] for i in range(0, len(raw_bits), 8)]
    message = ""

    for byte in raw_bytes:
        next_char = chr(int(byte, 2))
        message += next_char
        if next_char == delimiter:
            break

    return message[:-1]


def encode_bytes(message, img, delimiter='`'):
    width,height = img.size
    data = numpy.array(img)

    message = message.replace(delimiter, "")
    message += delimiter
    message_bytes = [format(ord(x), "08b") for x in message]
    curr_bit = 0
    curr_byte = 0

    for i in range(height):
        for j in range(width):
            pixel = data[i][j]
            r,g,b,*_ = map(lambda x: format(x, "08b"), pixel)

            # LSB
            # red pixel
            if curr_byte < len(message_bytes):
                pixel[0] = int(r[:-1] + message_bytes[curr_byte][curr_bit], 2)
                if curr_bit >= 7:
                    curr_bit = 0
                    curr_byte += 1
                else:
                    curr_bit += 1
            
            # green pixel
            if curr_byte < len(message_bytes):
                pixel[1] = int(g[:-1] + message_bytes[curr_byte][curr_bit], 2)
                if curr_bit >= 7:
                    curr_bit = 0
                    curr_byte += 1
                else:
                    curr_bit += 1

            # blue pixel
            if curr_byte < len(message_bytes):
                pixel[2] = int(b[:-1] + message_bytes[curr_byte][curr_bit], 2)
                if curr_bit >= 7:
                    curr_bit = 0
                    curr_byte += 1
                else:
                    curr_bit += 1
            else: break

    return Image.fromarray(data)

    #         # MSB FOR DEMONSTRATION PURPOSES ONLY
    #         # red pixel
    #         if curr_byte < len(message_bytes):
    #             pixel[0] = int(message_bytes[curr_byte][curr_bit] + r[1:] , 2)
    #             if curr_bit >= 7:
    #                 curr_bit = 0
    #                 curr_byte += 1
    #             else:
    #                 curr_bit += 1
            
    #         # green pixel
    #         if curr_byte < len(message_bytes):
    #             pixel[1] = int(message_bytes[curr_byte][curr_bit] + g[1:] , 2)
    #             if curr_bit >= 7:
    #                 curr_bit = 0
    #                 curr_byte += 1
    #             else:
    #                 curr_bit += 1

    #         # blue pixel
    #         if curr_byte < len(message_bytes):
    #             pixel[2] = int(message_bytes[curr_byte][curr_bit] + b[1:] , 2)
    #             if curr_bit >= 7:
    #                 curr_bit = 0
    #                 curr_byte += 1
    #             else:
    #                 curr_bit += 1
    #         else: break
    # return Image.fromarray(data)

root = tk.Tk()
root.withdraw()

while True:
    print("""
    Welcome to the Bootleg Steganography Service.
    Please select the service you'd like to use:
    1. Encode a message into an image
    2. Decode a message from an image
    3. Quit""")
    choice = input("\t Your Selection: ")

    if choice == "1":
        while True:
            message = input("\nEnter the message you want to encode, or press 1 again to choose a text file: ")

            if message == "1":
                text_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
                with open(text_file_path, 'r', encoding='utf-8') as f:
                    message = f.read()

                if not text_file_path:
                    message = ""
                    print("Cancelled or invalid")

            if message != "":
                print("\nYour message is {} bytes".format(len(message)))
                input("Press ENTER to select an image file to encode the data into: ")

                image_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
                img = Image.open(image_path)
                width, height = img.size
                max_load = int(width*height*3/8)    
                print("Opened a {0} x {1} px image".format(width, height))
                print("Max load for this image is {0} bytes".format(max_load))

                if max_load < len(message):
                    print("\nMessage too long for image resolution, message " +
                    "will be truncated to {} bytes".format(max_load))
                

                input("\nPress ENTER to begin encoding...")
                print("Encoding...")
                img2 = encode_bytes(message, img)
                print("Successfully encoded!")

                print("\nSelect name for output image file:")
                new_image_path = filedialog.asksaveasfilename(filetypes=[("PNG files", "*.png")])
                print("\nExporting to {}".format(new_image_path))
                img2.save(new_image_path)
                print("Done!")
                break
            
    elif choice == "2":
        input("\nPress ENTER to select an image file to decode: ")
        image_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        img = Image.open(image_path)      
        input("Successfully loaded image. Press ENTER to decode: ")

        message = decode_img(img)
        print("\nHere is the decoded message:\n\n")
        print(message)

    elif choice == "3":
        break
    else:
        print("\nInvalid choice, try again")