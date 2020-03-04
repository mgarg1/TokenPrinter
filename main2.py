# https://www.electronicwings.com/sensors-modules/mt8870-dtmf-decoder
# python -m virualenv proj/ --no-download -p python3
# python-escpos version which I am using:

import RPi.GPIO as GPIO
import time
from escpos.printer import Usb
import escpos.exceptions
from datetime import datetime
# from PIL import Image, ImageDraw
# import usb.core
# import usb.util
from textToImage import textToImage
from tokenMgr import getNextTokenNumber,writeToken 

SW1 = 40
LED_READY = 15
LED_ERROR = 13

def setupPrinter():
    printerObj = Usb(idVendor=0x0456, idProduct=0x0808, timeout=0, in_ep=0x81, out_ep=0x03)
    # printerObj = Dummy(idVendor=0x0456, idProduct=0x0808, timeout=0, in_ep=0x81, out_ep=0x03)
    print('printer found continuing')
    return printerObj
            
def setupGPIO():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    # GPIO.setup(OUTBITS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    # GPIO.setup(SW1, GPIO.IN)
    GPIO.setup(LED_READY, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(LED_ERROR, GPIO.OUT, initial=GPIO.LOW)

def printToken(printerObj,tokenCount):
    printerObj.hw("INIT")
    printerObj.control("LF")
    
    now = datetime.now() # current date and time
    imgObj = textToImage(tokenNum=tokenCount,dateVal=now.strftime('%d-%b-%Y'),timeVal=now.strftime('%H:%M:%S'))
    printerObj.image(imgObj,impl="bitImageColumn")
    printerObj.cut()

def setErrorLEDs(errorState=1):
    if errorState:
        GPIO.output(LED_READY, GPIO.LOW)
        GPIO.output(LED_ERROR, GPIO.HIGH)
    else:
        GPIO.output(LED_READY, GPIO.HIGH)
        GPIO.output(LED_ERROR, GPIO.LOW)

def checks():
    # find our device
    while usb.core.find(idVendor=0x0456, idProduct=0x0808) is None:
        pass

def mainLoop():
    setupGPIO()
    printerObj = setupPrinter()
    setErrorLEDs(0)
  
    while True: # Run forever
        try:
            # time.sleep(5)
            if GPIO.input(SW1) == GPIO.HIGH:
                setErrorLEDs(1)
                # TODO : implement this check
                # if printerObj.is_online() and printerObj.paper_status():
                if True:
                    tokenNum = getNextTokenNumber()
                    printToken(printerObj,str(tokenNum))
                    writeToken(tokenNum)
                    print("Button was pushed!")
                    time.sleep(5)

        except KeyboardInterrupt:
            GPIO.cleanup()
            printerObj.close()
            return

        except escpos.exceptions.USBNotFoundError as errorMsg:
            print(errorMsg)
            time.sleep(2)
            continue


mainLoop()
