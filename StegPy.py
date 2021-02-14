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

steg_mode = StringVar(root)
STEG_OPTIONS = ["LSB", "MSB"]

#ENCODE SECTION#
#-Input file row
input_png_file_label = Label(encode_tab, text="Input File Path:")
input_png_file_input = Entry(encode_tab, width=60)
input_png_file_button = Button(encode_tab, text="Browse...", command=lambda: open_file_path(input_png_file_input))

output_png_file_label = Label(encode_tab, text="Output File Path:")
output_png_file_input = Entry(encode_tab, width=60)
output_png_file_button = Button(encode_tab, text="Browse...", command=lambda: save_file_path(output_png_file_input))

steg_options_label = Label(encode_tab, text="Mode:")
steg_options_menu = OptionMenu(encode_tab, steg_mode, *STEG_OPTIONS)

encode_message = Listbox(encode_tab, height = 8, width = 60)
scrollbar = Scrollbar(encode_tab)
encode_message.configure(yscrollcommand = scrollbar.set)
scrollbar.configure(command = encode_message.yview)

input_png_file_label.grid(column=0, row=0) 
input_png_file_input.grid(column=1, row=0, columnspan=3) 
input_png_file_button.grid(column=4, row=0) 

output_png_file_label.grid(column=0, row=1) 
output_png_file_input.grid(column=1, row=1, columnspan=3) 
output_png_file_button.grid(column=4, row=1)

steg_options_label.grid(column=0, row=2)
steg_options_menu.grid(column=1, row=2)

encode_message.grid(row = 3, column = 0, columnspan = 3, pady = 10, padx = 10)
scrollbar.grid(row = 3, column = 3)


mainloop()