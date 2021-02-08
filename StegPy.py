from PIL import Image
import numpy
from tkinter import *
from tkinter import filedialog

def save_file_path(input_field):
    directory = filedialog.asksaveasfilename(filetypes=[("PNG files", "*.png")])
    input_field.delete(0, "end")
    input_field.insert(0, directory)

def open_file_path(input_field):
    directory = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    input_field.delete(0, "end")
    input_field.insert(0, directory)

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


root = Tk()
steg_mode = StringVar(root)
STEG_OPTIONS = ["LSB", "MSB"]

#DECODE SECTION#
#-Input file row
input_png_file_label = Label(root, text="Input File Path:")
input_png_file_input = Entry(root, width=60)
input_png_file_button = Button(root, text="Browse...", command=lambda: open_file_path(input_png_file_input))

output_png_file_label = Label(root, text="Output File Path:")
output_png_file_input = Entry(root, width=60)
output_png_file_button = Button(root, text="Browse...", command=lambda: save_file_path(output_png_file_input))

steg_options_label = Label(root, text="Mode:")
steg_options_menu = OptionMenu(root, steg_mode, *STEG_OPTIONS)

input_png_file_label.grid(column=0, row=0) 
input_png_file_input.grid(column=1, row=0) 
input_png_file_button.grid(column=2, row=0) 

output_png_file_label.grid(column=0, row=1) 
output_png_file_input.grid(column=1, row=1) 
output_png_file_button.grid(column=2, row=1)

steg_options_label.grid(column=0, row=2)
steg_options_menu.grid(column=1, row=2)

mainloop()