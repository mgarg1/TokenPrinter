# -*- coding: utf-8 -*- 

# https://code-maven.com/create-images-with-python-pil-pillow
from PIL import Image, ImageDraw, ImageFont
from os import path

import os
import sys

FONT_LOCATION = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static', 'fonts'))
# FONT_LOCATION = path.join('./','static','fonts')

def textToImage(tokenNum,dateVal='32-Dec-0019',timeVal='25:25:61',outFile=None):
    
    img = Image.new('RGB', (384, 220), color = (255, 255, 255))
     
    d = ImageDraw.Draw(img)
    unicode_fontDate = ImageFont.truetype(font=path.join(FONT_LOCATION,'ARIAL.TTF'),size=24)
    unicode_font30 = ImageFont.truetype(font=path.join(FONT_LOCATION,'Kruti_Dev.ttf'),size=48)

    yStart = 5

    # This EveryCom printer is 203DPI (pixel per inch)
    # 1 pixel is 1/203 inch
    # 100 pixel is 1/2 inch
    # 384 Pixels/Line

    # HEADER - Date and Time
    d.text((5,yStart), dateVal, font=unicode_fontDate, fill=(0,0,0))
    dateTextSize = d.textsize(timeVal,font=unicode_fontDate) 
    d.text((384-dateTextSize[0]-10,yStart), timeVal, font=unicode_fontDate, fill=(0,0,0))
    
    yStart = yStart+dateTextSize[1]+10
    # http://indiatyping.com/index.php/font-converter/unicode-to-krutidev-font-converter
    TOKEN_CONTENT = 'e;wjh g‚fLiVy\nVksdu u-\n%s\nAAlosZ lUrq fujke;kAA' % (str(tokenNum))
    d.text(((384/2-d.multiline_textsize(TOKEN_CONTENT,font=unicode_font30)[0]/2),yStart), TOKEN_CONTENT, font=unicode_font30, fill=(0,0,0),align='center')

    if outFile:
        img.save(outFile)

    return img