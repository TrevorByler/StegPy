import PIL.Image
import numpy
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

def save_file_path(input_field: Entry):
    directory = filedialog.asksaveasfilename(filetypes=[("PNG files", "*.png")])
    input_field.delete(0, "end")
    input_field.insert(0, directory)

def open_file_path(input_field: Entry):
    directory = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
    input_field.delete(0, "end")
    input_field.insert(0, directory)

def import_text(textbox: Text):
    text_file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    with open(text_file_path, 'r', encoding='utf-8') as f:
        message = f.readlines()
        textbox.delete(1.0, END)
        for line in message:
            textbox.insert(END, line)

def decode_img(img: PIL.Image, delimiter='``') -> str:
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


def encode_bytes(message: str, img: PIL.Image, delimiter='``') -> PIL.Image :
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

    return PIL.Image.fromarray(data)

def write_to_file(input_field: Entry, output_field: Entry, text: Listbox):
        message = "".join(text.get(0, last=END))
        print(message)
        img = PIL.Image.open(input_field.get())
        img2 = encode_bytes(message, img)
        img2.save(output_field.get())

def decode_file(input_field: Entry, display: Text):
    img = PIL.Image.open(input_field.get())
    display.delete(1.0, END)
    message = decode_img(img)
    display.insert(END, message)

root = Tk()
root.title("StegoPy")

tab_control = ttk.Notebook(root)
decode_tab = ttk.Frame(tab_control)
encode_tab = ttk.Frame(tab_control)
tab_control.add(encode_tab, text="Encode")
tab_control.add(decode_tab, text="Decode")
tab_control.pack(expand = TRUE, fill = BOTH)

# ENCODE SECTION 
# -Input file row
input_png_file_frame = Frame(encode_tab)
input_png_file_label = Label(input_png_file_frame, text="Input File Path:")
input_png_file_input = Entry(input_png_file_frame)
input_png_file_button = Button(input_png_file_frame, text="Browse...",
                                command=lambda: open_file_path(input_png_file_input))

# --setup input frame
input_png_file_label.pack(side = LEFT)
input_png_file_input.pack(side = LEFT, expand = TRUE, fill = X)
input_png_file_button.pack(side = LEFT)

# -Output file row
output_png_file_frame = Frame(encode_tab)
output_png_file_label = Label(output_png_file_frame, text="Output File Path:")
output_png_file_input = Entry(output_png_file_frame)
output_png_file_button = Button(output_png_file_frame, text="Browse...",
                                command=lambda: save_file_path(output_png_file_input))

# --setup output frame
output_png_file_label.pack(side = LEFT)
output_png_file_input.pack(side = LEFT, expand = TRUE, fill = X)
output_png_file_button.pack(side = LEFT)


# -Message box
encode_textbox_frame = Frame(encode_tab)
encode_textbox = Text(encode_textbox_frame, wrap = WORD)
encode_scrollbar_y = Scrollbar(encode_textbox_frame)
encode_scrollbar_x = Scrollbar(encode_textbox_frame, orient = HORIZONTAL)

encode_textbox.configure(yscrollcommand = encode_scrollbar_y.set, xscrollcommand = encode_scrollbar_x.set)
encode_scrollbar_y.configure(command = encode_textbox.yview)
encode_scrollbar_x.configure(command = encode_textbox.xview)

import_text_button = Button(encode_textbox_frame, text="Import Text File",
                            command=lambda: import_text(encode_textbox))

# --set up message box frame
import_text_button.pack(side = TOP)
encode_scrollbar_x.pack(side = BOTTOM, fill = X)
encode_scrollbar_y.pack(side = RIGHT, fill = Y)
encode_textbox.pack(side = TOP, expand = TRUE, fill = BOTH)

# -Encode Button
encode_commit_button = Button(encode_tab, text = "Encode",
        command = lambda: write_to_file(input_png_file_input, output_png_file_input, encode_textbox))

# -Pack frames and button into tab
input_png_file_frame.pack(side = TOP, expand = TRUE, fill = BOTH)
output_png_file_frame.pack(side = TOP, expand = TRUE, fill = BOTH)
encode_textbox_frame.pack(side = TOP, expand = TRUE, fill = BOTH)
encode_commit_button.pack(side = BOTTOM)

# DECODE SECTION 
# -decode file row
decode_png_file_frame = Frame(decode_tab)
decode_png_file_label = Label(decode_png_file_frame, text="Select File to Decode:")
decode_png_file_input = Entry(decode_png_file_frame)
decode_png_file_button = Button(decode_png_file_frame, text="Browse...",
                                command=lambda: open_file_path(decode_png_file_input))

# --setup decode frame
decode_png_file_label.pack(side = LEFT)
decode_png_file_input.pack(side = LEFT, expand = TRUE, fill = X)
decode_png_file_button.pack(side = LEFT)

# -Decode Output
decode_textbox_frame = Frame(decode_tab)
decode_textbox = Text(decode_textbox_frame, wrap = WORD)
decode_scrollbar_y = Scrollbar(decode_textbox_frame)

decode_textbox.configure(yscrollcommand = decode_scrollbar_y.set, xscrollcommand = encode_scrollbar_x.set)
decode_scrollbar_y.configure(command = decode_textbox.yview)

# --setup textbox frame
decode_scrollbar_y.pack(side = RIGHT, fill = Y)
decode_textbox.pack(side = TOP, expand = TRUE, fill = BOTH)

decode_button = Button(decode_tab, text = "Decode",
                        command = lambda: decode_file(decode_png_file_input, decode_textbox))

decode_png_file_frame.pack(side = TOP, expand = TRUE, fill = BOTH)
decode_textbox_frame.pack(side = TOP, expand = TRUE, fill = BOTH)
decode_button.pack(side = TOP)

mainloop()