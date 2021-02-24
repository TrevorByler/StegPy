from PIL import Image
import numpy
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

def save_file_path(input_field):
    directory = filedialog.asksaveasfilename(filetypes=[("PNG files", "*.png")])
    input_field.delete(0, "end")
    input_field.insert(0, directory)

def open_file_path(input_field):
    directory = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    input_field.delete(0, "end")
    input_field.insert(0, directory)

def import_text(listbox):
    text_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    with open(text_file_path, 'r', encoding='utf-8') as f:
        message = f.readlines()
        listbox.delete(0, END)
        for line in message:
            listbox.insert(END, line)

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
root.title("StegoPy")

tab_control = ttk.Notebook(root)
decode_tab = ttk.Frame(tab_control)
encode_tab = ttk.Frame(tab_control)
tab_control.add(encode_tab, text="Encode")
tab_control.add(decode_tab, text="Decode")
tab_control.pack(expand=1, fill="both")

steg_mode = IntVar(encode_tab)
STEG_OPTIONS = [("LSB", 1), ("MSB", 2)]

# ENCODE SECTION#
# -Input file row
input_png_file_frame = Frame(encode_tab)
input_png_file_label = Label(input_png_file_frame, text="Input File Path:")
input_png_file_input = Entry(input_png_file_frame)
input_png_file_button = Button(input_png_file_frame, text="Browse...", command=lambda: open_file_path(input_png_file_input))

input_png_file_label.pack(side = LEFT)
input_png_file_input.pack(side = LEFT, expand = TRUE, fill = X)
input_png_file_button.pack(side = LEFT)

output_png_file_frame = Frame(encode_tab)
output_png_file_label = Label(output_png_file_frame, text="Output File Path:")
output_png_file_input = Entry(output_png_file_frame)
output_png_file_button = Button(output_png_file_frame, text="Browse...", command=lambda: save_file_path(output_png_file_input))

output_png_file_label.pack(side = LEFT)
output_png_file_input.pack(side = LEFT, expand = TRUE, fill = X)
output_png_file_button.pack(side = LEFT)

# steg_options_label = Label(encode_tab, text="Mode:")

encode_textbox_frame = Frame(encode_tab)
encode_textbox = Listbox(encode_textbox_frame)
scrollbar_y = Scrollbar(encode_textbox_frame)
scrollbar_x = Scrollbar(encode_textbox_frame, orient = HORIZONTAL)

encode_textbox.configure(yscrollcommand = scrollbar_y.set, xscrollcommand = scrollbar_x.set)
scrollbar_y.configure(command = encode_textbox.yview)
scrollbar_x.configure(command = encode_textbox.xview)

import_text_button = Button(encode_textbox_frame, text="Import Text File", command=lambda: import_text(encode_textbox))

import_text_button.pack(side = TOP)
import_text_button.pack_configure()
scrollbar_x.pack(side = BOTTOM, fill = X)
scrollbar_y.pack(side = RIGHT, fill = Y)
encode_textbox.pack(side = TOP, expand = TRUE, fill = BOTH)

input_png_file_frame.pack(side = TOP, expand = TRUE, fill = BOTH)
output_png_file_frame.pack(side = TOP, expand = TRUE, fill = BOTH)
encode_textbox_frame.pack(side = TOP, expand = TRUE, fill = BOTH)

# steg_options_label.grid(column=0, row=2)
# for i, option in enumerate(STEG_OPTIONS):
#     Radiobutton(encode_tab, text=option[0],
#                 variable=steg_mode, value=option[1]).grid(column=i+1, row=2, sticky=W)

mainloop()