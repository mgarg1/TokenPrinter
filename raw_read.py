import time
from escpos.printer import Usb
# import escpos.exceptions
# from datetime import datetime
# from PIL import Image, ImageDraw


# ESC @
printerObj = Usb(0x0456, 0x0808, 0, 0x81, 0x03)
# msg1=b'\x48\x65\x6c\x6c\x6f\x2c\x20\x50\x68\x6f\x65\x6e\x69\x78\x20\x70\x72\x69\x6e\x74\x65\x72\x21'

disableBut=b'\x1B\x63\x35\x00'
macroDef=b'\x1D\x3A'
helloMsg=b'\x48\x65\x6c\x6c\x6f\x0A\x0A\x0A\x0A'
macroExc=b'\x1D\x5E\x03\x0A\x01'

msg22 = disableBut+macroDef+helloMsg+macroDef
# msg22 = disableBut
# msg=b'\x10\x04\x04'
# printerObj.device.write(printerObj.out_ep,macroExc)

# time.sleep(2)

# printerObj.device.write(printerObj.out_ep,macroExc)

msgDLEENQ=b'\x10\x05\x00'
printerObj.device.write(printerObj.out_ep,msgDLEENQ)


aa = printerObj.device.read(printerObj.out_ep,1)
# print(aa)
# e.device.read(e.ep_out,1)
