# -*- coding: utf-8 -*- 

# https://code-maven.com/create-images-with-python-pil-pillow
from PIL import Image, ImageDraw, ImageFont
from os import path

FONT_LOCATION = path.join('./','static','fonts')

def txtToImg(tokenNum,dateVal='32-Dec-0019',timeVal='25:25:61',outFile='tokenImg.png'):
    
    img = Image.new('RGB', (237, 112), color = (255, 255, 255))
     
    d = ImageDraw.Draw(img)
    unicode_fontDate = ImageFont.truetype(font=path.join(FONT_LOCATION,'ARIAL.TTF'),size=12)
    unicode_font10 = ImageFont.truetype(font=path.join(FONT_LOCATION,'Kruti_Dev.ttf'),size=18)
    unicode_font30 = ImageFont.truetype(font=path.join(FONT_LOCATION,'Kruti_Dev.ttf'),size=30)

    yStart = 5
    # HEADER - Date and Time
    d.text((5,yStart), dateVal, font=unicode_fontDate, fill=(0,0,0))
    d.text((155,yStart), timeVal, font=unicode_fontDate, fill=(0,0,0))
    
    # http://indiatyping.com/index.php/font-converter/unicode-to-krutidev-font-converter
    d.text((50,yStart+13), 'e;wjh g‚fLiVy', font=unicode_font30, fill=(0,0,0))
    d.text((75,yStart+40), 'Vksdu u-', font=unicode_font30, fill=(0,0,0))
    d.text((100,yStart+60), str(tokenNum), font=unicode_font30, fill=(0,0,0))

    # FOOTER
    d.text((45,yStart+85), u'AA losZ lUrq fujke;k AA', font=unicode_font10, fill=(0,0,0))
    img.save(outFile)



txtToImg(23)
