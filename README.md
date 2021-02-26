# StegPy v0.1

Hide your own data in PNG files with LSB stegonography. Uses Python's Pillow image processing library and numpy to encode and decode stego-images. Tkinter provides the GUI framework.
Created by Trevor Byler

## Features

- [x] Basic LSB encoding
- [x] GUI
- [ ] High-capacity LSB encoding
- [ ] Alpha-channel support
- [ ] Warning and success message pop-ups
- [ ] More image formats
- [ ] Encode images into images
- [ ] Whatever I think of next

## Directions for Use

### Encoding Data

1.  Save the text data you want to encode into a .txt file.
2.  Save a cover image as a .png file
3.  In the StegPy program, click the "Encode" tab and select the cover image in the "Input File Path" field
4.  Select the output file path in the next field
5.  Click "Import Text File" to bring in the text data you saved earlier
6.  Click "Encode" to create the stego-image

### Decoding Data

1.  Click on the "Decode" tab
2.  Select the stego-image file path in the "Select File to Decode" field
3.  Click "Decode" at the bottom of the window
4.  The hidden message will be displayed in the text box

## Technical Details

- This version of LSB encoding uses 3 bits per RGB pixel
- Therefore, it takes 8 pixels to store 3 characters worth of data
- If there are not enough pixels in the cover image to store the message, the message will be truncated
- The program adds a delimiter to the message to mark the end of the message. The default delimeter is a double backtick ( `` )
- If the message contains the delimiter, the entire message will be encoded, but decoding will stop at the first occurrence of the delimiter.
