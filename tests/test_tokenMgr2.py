import context

from datetime import datetime,timedelta
from tokenMgr2 import getNextTokenNumber,writeToken,DATE_FORMAT,TOKEN_START,TOKEN_DELTA
from eeprom import clearEEPROM
import os

def cleanup():
    #os.remove(LAST_TOKEN_FILENAME)
    #os.remove(LAST_DATE_FILENAME)
    pass

# Test to check if two consecutive getNextTokenNumber return right results
def testToken1():
    clearEEPROM()
    writeToken(2)
    token = getNextTokenNumber()
    print('recvdToken - ' + str(token))
    assert token != None, "token number cannot be None"
    writeToken(token)
    
    token2 = getNextTokenNumber()
    print('recvdToken - ' + str(token2))
    assert token2 == token+TOKEN_DELTA, "token number is not updated on write"
    cleanup()

# Test to check if reset of token number works on day change
def testToken2():
    token = getNextTokenNumber()
    writeToken(token)
    token = getNextTokenNumber()
    writeToken(token)
    token = getNextTokenNumber()
    writeToken(token)

    todayDate = datetime.now()
    onedaydelta = timedelta(days=1)
    nextDay=todayDate+onedaydelta
    
    token2 = getNextTokenNumber(nextDay)
    assert token2 == TOKEN_START,"nextDay token resetting not working"
    cleanup()

testToken1()
testToken2()
