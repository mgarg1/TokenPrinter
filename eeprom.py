# https://www.raspberrypi.org/forums/viewtopic.php?t=215510

import time
import smbus

EEPROMbus = smbus.SMBus(1)
Device_Address = 0x57 #note EEPROM address may be 0X56
EEPROM_DELAY = 0.10

'''
Check your EEPROM address using: sudo i2cdetect -y 1

  AT24C32 Code
  datasheet: atmel.com/Images/doc0336.pdf
  '''
def set_current_AT24C32_address(EEPROM_Memory_Address):
    a1 = int(EEPROM_Memory_Address/256)
    a0 = int(EEPROM_Memory_Address % 256)

    EEPROMbus.write_i2c_block_data(Device_Address, a1, [a0])
    return;

def read_AT24C32_byte(EEPROM_Memory_Address):

    set_current_AT24C32_address(EEPROM_Memory_Address)
    return EEPROMbus.read_byte(Device_Address);

def write_AT24C32_block(EEPROM_Address, value):
    a1 = int(EEPROM_Address/256)
    a0 = int(EEPROM_Address % 256)

    EEPROMbus.write_i2c_block_data(Device_Address, a1, [a0, value])
    time.sleep(EEPROM_DELAY)
    return;

def write_AT24C32_byte(EEPROM_Memory_Address, value):
    EEPROMbus.write_byte_data(Device_Address, EEPROM_Memory_Address, value)
    time.sleep(EEPROM_DELAY)
    return;

def reset():
    EEPROMbus.write_byte_data(Device_Address,0xA5,0x5A)
    #write_AT24C32_byte(0xA5,0x5A)

#example of storing string values into the EEPROM
#sString = "Bad Boys Race Our Young Girls Over Victory Garden Walls Get Started Now"
#iStartingAddress = 0 #next starting address
#iEndingAddress = 0
#
'''
write

'''
#print ("Ending Address, used as starting address of next data: " +  str(iEndingAddress))

def writeString(startAddr,inputStr):
    byteArray = bytearray()
    byteArray.extend(inputStr.encode())
    iEndingAddress = 0
    
    for byteVal in byteArray:
        write_AT24C32_block(startAddr+iEndingAddress, byteVal)
        #print(byteVal)
        iEndingAddress = iEndingAddress + 1

'''
read

'''
def readString(startAddr,numOfBytes):
    sString = ""
    sTemp = b""
    for iX in range(startAddr, startAddr+numOfBytes):
        sTemp = bytes([read_AT24C32_byte(iX)]) #note the [ ]
        #print(sTemp,sTemp.decode('utf-8'))
        sString = sString + sTemp.decode('utf-8')
    
    print(sString)
    return sString

def clearEEPROM():
    byteArray = bytearray(100)
    #byteArray.extend(inputStr.encode())
    iEndingAddress = 0
    
    for byteVal in byteArray:
        write_AT24C32_block(iEndingAddress, byteVal)
        #print(byteVal)
        iEndingAddress = iEndingAddress + 1



#sString = "Bad Boys Race Our Young Girls Over Victory Garden Walls Get Started NowBad Boys Race Our Young Girls Over Victory Garden Walls Get Started Now"
#writeString(0,sString)
#readString(0,3)
#reset()
#readString(0,3)
