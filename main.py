# https://www.electronicwings.com/sensors-modules/mt8870-dtmf-decoder
# python -m virualenv proj/ --no-download -p python3
# python-escpos version which I am using:

import RPi.GPIO as GPIO
import time
from escpos.printer import Usb
import escpos.exceptions
from datetime import datetime
from PIL import Image, ImageDraw
import usb.core
# import usb.util


SW1 = 40
LED_READY = 2
LED_ERROR = 3

TOKEN_START = 12
TOKEN_DELTA = 2
LAST_TOKEN_FILENAME = "lastToken.txt"
LAST_DATE_FILENAME = "lastDate.txt"


def setupFiles(filename):
    fileh = open(filename, 'a')
    try:
        pass
    finally:
        fileh.close()

def getNextTokenNumber():
    with open(LAST_DATE_FILENAME,'r+',encoding = 'utf-8') as dateFile:
        lastDay = dateFile.read().strip()
        now = datetime.now() # current date and time
        now_day = now.strftime("%d-%b-%Y").strip()

        lastToken = TOKEN_START
        with open(LAST_TOKEN_FILENAME,'r+',encoding = 'utf-8') as tokenFile:
            # print(now_day)
            # print(lastDay)
            if lastDay == now_day:
                # print("day hasn't changed")
                lastToken = tokenFile.read()
                lastToken = int(lastToken) + TOKEN_DELTA
            
            tokenFile.truncate(0)
            tokenFile.seek(0)
            tokenFile.write(str(lastToken))
        dateFile.truncate(0)
        dateFile.seek(0)
        dateFile.write(now_day)
        return lastToken

def setupPrinter():

    # find our device
    # while usb.core.find(idVendor=0x0456, idProduct=0x0808) is None:
        # pass
    while True:
        try:
            printerObj = Usb(idVendor=0x0456, idProduct=0x0808, timeout=0, in_ep=0x81, out_ep=0x03)
            printerObj = Dummy(idVendor=0x0456, idProduct=0x0808, timeout=0, in_ep=0x81, out_ep=0x03)
            # printerObj = Usb(0x0456, 0x0808, 0, 0x81, 0x03)
            print('printer found continuing')
            return printerObj
            # printerObj.panel_buttons(enable=False)
        # return printerObj
        except escpos.exceptions.USBNotFoundError as errorMsg:
            print(errorMsg)
            time.sleep(2)
            continue

def printDate(printerObj):
    now = datetime.now() # current date and time
    now_time = now.strftime("%d-%b-%Y       %H:%M:%S")
    printerObj.set(height=1, width=1)
    printerObj.text(now_time)
    printerObj.control("CR")

def printToken(printerObj,tokenCount):
    printerObj.hw("INIT")
    printerObj.control("LF")
    printDate(printerObj)
    
    printerObj.image("static/sleet3.png",impl="bitImageColumn")
    printerObj.set(width=3,align='center')
    printerObj.text(tokenCount)
    printerObj.text("\n\n")
    printerObj.image("static/footer.png",impl="bitImageColumn")
    # TODO : not sure if it needs to be here
    # printerObj.set(font='a', height=1, width=1, align='center')
    printerObj.text("\n\n\n\n")
    # printerObj.print_and_feed(n=1)
    printerObj.hw("INIT")
    # printerObj.cut()

def setupGPIO():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    # GPIO.setup(OUTBITS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
    # GPIO.setup(SW1, GPIO.IN)
    GPIO.setup(LED_READY, GPIO.OUT, initial=GPIO.HIGH)
    GPIO.setup(LED_ERROR, GPIO.OUT, initial=GPIO.LOW)

def setErrorLEDs(errorState=1):
    if errorState:
        GPIO.output(LED_READY, GPIO.LOW)
        GPIO.output(LED_ERROR, GPIO.HIGH)
    else:
        GPIO.output(LED_READY, GPIO.HIGH)
        GPIO.output(LED_ERROR, GPIO.LOW)


def mainLoop():
    setupGPIO()
    printerObj = setupPrinter()
    setupFiles(LAST_DATE_FILENAME)
    setupFiles(LAST_TOKEN_FILENAME)

    while True: # Run forever
        try:
            setErrorLEDs(0)
            # time.sleep(5)
            if GPIO.input(SW1) == GPIO.HIGH:
                setErrorLEDs(1)
                # TODO : implement this check
                # if printerObj.is_online() and printerObj.paper_status():
                if True:
                    printToken(printerObj,str(getNextTokenNumber()))
                    print("Button was pushed!")
                    time.sleep(5)

        except KeyboardInterrupt:
            GPIO.cleanup()
            printerObj.close()
            return

mainLoop()

      