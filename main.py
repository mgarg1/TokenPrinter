# https://www.electronicwings.com/sensors-modules/mt8870-dtmf-decoder
# python -m virualenv proj/ --no-download -p python3

import logging
logging.basicConfig(
        format='%(asctime)s - %(levelname)s - %(message)s - %(funcName)s - line %(lineno)d',
        level=logging.DEBUG)
#logging.disable(logging.CRITICAL)

import RPi.GPIO as GPIO
import time
from escpos.printer import Usb,File
import escpos.exceptions
from datetime import datetime
# from PIL import Image, ImageDraw
# import usb.core
# import usb.util
from textToImage import textToImage
from tokenMgr import getNextTokenNumber,writeToken 

#logger = logging.getLogger()
#log_handler = logging.StreamHandler(sys.stdout)
#log_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s - %(funcName)s - line %(lineno)d"))
#log_handler.setLevel(logging.INFO)
#logger.addHandler(log_handler)
logging.disable(logging.NOTSET)

SW1 = 16

LED_READY = 8
LED_ERROR = 13

def setupPrinter():
    # To find the VendorId and ProductId of the connected printer:
    # $ lsusb
    # Bus 001 Device 011: ID 0456:0808 Analog Devices, Inc.

    # To find the Endpoints
    # $ sudo lsusb -v -d 0456:0808
    #
    #  Endpoint Descriptor:
    #    bEndpointAddress     0x81  EP 1 IN
    #  Endpoint Descriptor:
    #    bEndpointAddress     0x03  EP 3 OUT
 
    # find our device
    # while usb.core.find(idVendor=0x0456, idProduct=0x0808) is None:
        # pass

    printerObj = File('/dev/usb/lp0')
    #printerObj = Usb(idVendor=0x0456, idProduct=0x0808, timeout=0, in_ep=0x81, out_ep=0x03)
    # printerObj = Dummy(idVendor=0x0456, idProduct=0x0808, timeout=0, in_ep=0x81, out_ep=0x03)
    logging.debug("printer found continuing")
    return printerObj
    # printerObj.panel_buttons(enable=False)
    # return printerObj

def printToken(printerObj,tokenCount):
    #printerObj.hw("RESET")
    #printerObj.hw("INIT")
    printerObj.control("LF")
    
    now = datetime.now() # current date and time
    imgObj = textToImage(tokenNum=tokenCount,dateVal=now.strftime('%d-%b-%Y'),timeVal=now.strftime('%H:%M:%S'))
    #printerObj.image('tests/baseLine_textToImage.png')
    imgObj.save('/tmp/imgToken.png')
    printerObj.image('/tmp/imgToken.png')
    #,impl="bitImageColumn")
    # printerObj.text('HELLO MOHIT')
    printerObj.cut()

def setupGPIO():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    # GPIO.setup(OUTBITS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(SW1, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
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
    setupRequired = True
    printerObj = None  
    while True: # Run forever
        try:
            if setupRequired:
                setupGPIO()
                printerObj = setupPrinter()
                setupRequired = False
                setErrorLEDs(0)

            # time.sleep(5)
            if GPIO.input(SW1) == GPIO.LOW:
                setErrorLEDs(1)
                # TODO : implement this check
                # if printerObj.is_online() and printerObj.paper_status():
                if True:
                    tokenNum = getNextTokenNumber()
                    printToken(printerObj,str(tokenNum))
                    writeToken(tokenNum)
                    logging.debug("Button was pushed!")
                    time.sleep(5)
                    setErrorLEDs(0)
                time.sleep(0.2)

        except KeyboardInterrupt:
            # Exit on Ctrl-c
            GPIO.cleanup()
            if printerObj:
                printerObj.close()
            return

        except (escpos.exceptions.USBNotFoundError,escpos.exceptions.Error) as errorMsg:
            setErrorLEDs(1)
            if printerObj:
                printerObj.close()
            
            logging.warning("escpos recognized error")
            logging.warning(str(errorMsg))
            setupRequired = True
            time.sleep(2)
            # continue
        except Exception as errorMsg:
            logging.exception(str(errorMsg))
            if printerObj:
                printerObj.close()
mainLoop()
