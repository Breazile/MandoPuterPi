"""
This demo will draw a few rectangles onto the screen along with some text
on top of that.

This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!

Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""
import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import

#DISPLAY       = "1.14 LCD"                           # Adafruit 1.14" LCD display  https://www.adafruit.com/product/4383
DISPLAY       = "1.3 LCD"                            # Adafruit 1.3" LCD display   https://www.adafruit.com/product/4313
glyphlist     = [ "MLM", "FBM", "SAS", "FAS", "TRH"] # Mandalorian charater sequence that is shown on the display
glyphdelays   = [  0.50,  0.50,  0.50,  0.50,  0.50] # Time that each character group is shown 0.50 is 500 milliseconds, or 1/2 of a second
graphiclist   = [ ]
#graphiclist   = [ "m1.jpg", "m2.jpg", "m3.jpg", "m4.jpg", "m5.jpg"]
graphicdelays = [      1.0,      1.0,      1.0,      1.0,      1.0]

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000
#BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()
# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# pylint: disable=line-too-long
# Create the display:
if DISPLAY == "1.14 LCD":
  FONTSIZE = 124
  disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE)
elif DISPLAY == "1.3 LCD":
  FONTSIZE = 180
  disp = st7789.ST7789(spi, width=240, height=240, y_offset=80, rotation=0, cs=cs_pin, dc=dc_pin, rst=reset_pin, baudrate=BAUDRATE)
    
# pylint: enable=line-too-long

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height

# Load the Mandalorian TrueType Font
font = ImageFont.truetype("./mandalor.ttf", FONTSIZE)

# font rendering function, center text on the screen
def render_font(glyphlist, image):
   # Get drawing object to draw on image.
   draw = ImageDraw.Draw(image)
   # Draw a black background
   draw.rectangle((0, 0, width, height), fill=(0, 0, 0))
   #disp.image(image)
   # Draw Some Text
   (font_width, font_height) = font.getsize(glyphlist)
   draw.text((width // 2 - font_width // 2, height // 2 - font_height // 2), glyphlist, font=font, fill=(255, 0, 0))

# render each sequence of characters using the bitmap font
txtglyphs = []
index = 0
for msg in glyphlist:
    txtglyphs.append(Image.new("RGB", (width, height)))
    render_font(msg, txtglyphs[index])
    index = index + 1

#load images
imgglyphs = []
index = 0
for filename in graphiclist:
    imgglyphs.append(Image.open(filename))

    # Scale the image to the smaller screen dimension
    image_ratio = imgglyphs[index].width / imgglyphs[index].height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = imgglyphs[index].width * height // imgglyphs[index].height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = imgglyphs[index].height * width // imgglyphs[index].width
    imgglyphs[index] = imgglyphs[index].resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    imgglyphs[index] = imgglyphs[index].crop((x, y, x + width, y + height))
    index = index + 1

# loop through and display the fonts and images
while True:
    index = 0
    for glyph in txtglyphs:
        disp.image(glyph)
        time.sleep(glyphdelays[index])
        index = index + 1
    index = 0
    for img in imgglyphs:
        disp.image(img)
        time.sleep(graphicdelays[index])
        index = index + 1
