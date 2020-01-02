# https://www.electronicwings.com/sensors-modules/mt8870-dtmf-decoder
# python -m virualenv proj/ --no-download -p python3
# python-escpos version which I am using:

import RPi.GPIO as GPIO
import time
from escpos.printer import Usb
import escpos.exceptions
from datetime import datetime
# from PIL import Image, ImageDraw
import usb.core
# import usb.util
from textToImage import textToImage 

SW1 = 40
LED_READY = 15
LED_ERROR = 13

TOKEN_START = 12
TOKEN_DELTA = 2
LAST_TOKEN_FILENAME = "lastToken.txt"
LAST_DATE_FILENAME = "lastDate.txt"
DATE_FORMAT = "%d-%b-%Y"

def setupFiles(filename):
    fileh = open(filename, 'a')
    try:
        pass
    finally:
        fileh.close()

def readFile(filename):
    fileContent=None
    with open(filename,'r',encoding = 'utf-8') as fileh:
        fileContent = fileh.read().strip()

    return fileContent

def writeFile(filename,fileContent):
    # filemode is 'w' -> if exist then truncate, otherwise create
     with open(filename,'w',encoding = 'utf-8') as fileh:
        fileh.write(fileContent)

def updateFiles(tokenNum,lastDay=datetime.now().strftime(DATE_FORMAT).strip()):
    writeFile(LAST_TOKEN_FILENAME,tokenNum)
    writeFile(LAST_DATE_FILENAME,lastDay)


def getNextTokenNumber2():
    lastDay = readFile(LAST_DATE_FILENAME)
    lastToken = readFile(LAST_TOKEN_FILENAME)

    curr_day = datetime.now().strftime(DATE_FORMAT).strip()
    if lastDay == curr_day:
        curr_Token = int(lastToken) + TOKEN_DELTA
    else:
        curr_Token = TOKEN_START

    return lastToken

# def getNextTokenNumber():
#     with open(LAST_DATE_FILENAME,'r+',encoding = 'utf-8') as dateFile:
#         lastDay = dateFile.read().strip()
#         now = datetime.now() # current date and time
#         now_day = now.strftime(DATE_FORMAT).strip()
# 
#         lastToken = TOKEN_START
#         with open(LAST_TOKEN_FILENAME,'r+',encoding = 'utf-8') as tokenFile:
#             # print(now_day)
#             # print(lastDay)
#             if lastDay == now_day:
#                 # print("day hasn't changed")
#                 lastToken = tokenFile.read()
#                 lastToken = int(lastToken) + TOKEN_DELTA
#             
#             tokenFile.truncate(0)
#             tokenFile.seek(0)
#             tokenFile.write(str(lastToken))
#         dateFile.truncate(0)
#         dateFile.seek(0)
#         dateFile.write(now_day)
#         return lastToken

def setupPrinter():

    # find our device
    # while usb.core.find(idVendor=0x0456, idProduct=0x0808) is None:
        # pass
    while True:
        try:
            printerObj = Usb(idVendor=0x0456, idProduct=0x0808, timeout=0, in_ep=0x81, out_ep=0x03)
            # printerObj = Dummy(idVendor=0x0456, idProduct=0x0808, timeout=0, in_ep=0x81, out_ep=0x03)
            # printerObj = Usb(0x0456, 0x0808, 0, 0x81, 0x03)
            print('printer found continuing')
            return printerObj
            # printerObj.panel_buttons(enable=False)
        # return printerObj
        except escpos.exceptions.USBNotFoundError as errorMsg:
            print(errorMsg)
            time.sleep(2)
            continue

def printToken(printerObj,tokenCount):
    printerObj.hw("INIT")
    printerObj.control("LF")
    
    now = datetime.now() # current date and time
    imgObj = textToImage(tokenNum=tokenCount,dateVal=now.strftime('%d-%b-%Y'),timeVal=now.strftime('%H:%M:%S'))
    printerObj.image(imgObj,impl="bitImageColumn")
    printerObj.cut()

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
                    tokenNum = getNextTokenNumber()
                    printToken(printerObj,str(tokenNum))
                    updateFiles(str(tokenNum))
                    print("Button was pushed!")
                    time.sleep(5)

        except KeyboardInterrupt:
            GPIO.cleanup()
            printerObj.close()
            return

mainLoop()
