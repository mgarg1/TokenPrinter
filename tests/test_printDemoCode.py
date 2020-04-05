
from escpos.printer import Usb,Serial


""" Seiko Epson Corp. Receipt Printer (EPSON TM-T88III) """
#p = Serial(u'/dev/usb/lp0')
p = Usb(idVendor=0x0456, idProduct=0x0808, timeout=0, in_ep=0x81, out_ep=0x03)
#p = Usb(0x04b8, 0x0202, 0, profile="TM-T88III")
p.hw('RESET')
#p.control('LF')
p.text("Hello World \n kdfjlsjflskdjflj \n sfsdfsdf \n sdfsdfsdfsd \n sdfsdfsdfdsf")
#p.image("logo.gif")
#p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
#p.cut()
p.cut()
p.close()
