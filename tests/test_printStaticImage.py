from escpos.printer import Usb
# some_file.py
from datetime import datetime
import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')
import textToImage

def setupPrinter():
    printerObj = Usb(idVendor=0x0456, idProduct=0x0808, timeout=0, in_ep=0x81, out_ep=0x03)
    print('printer found continuing')
    return printerObj
   
def printImage(printerObj):
    # https://python-escpos.readthedocs.io/en/latest/api/escpos.html#escpos.escpos.Escpos.image
    tokenCount = 23
    now = datetime.now() # current date and time
    imgObj = textToImage.textToImage(tokenNum=tokenCount,dateVal=now.strftime('%d-%b-%Y'),timeVal=now.strftime('%H:%M:%S'))
    printerObj.image(imgObj)
            #impl="bitImageColumn")
    # printerObj.text("\n\n")
    printerObj.cut()

def mainLoop():
    printerObj = None
    try:
        printerObj = setupPrinter()
        printImage(printerObj)
    except Exception as e:
        if printerObj:
            printerObj.close()
        print(str(e))

mainLoop() 
