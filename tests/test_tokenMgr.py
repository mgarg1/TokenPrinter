import sys
sys.path.insert(0, '../')

from datetime import datetime,timedelta
from tokenMgr import getNextTokenNumber,writeToken,DATE_FORMAT,TOKEN_START,TOKEN_DELTA 

# Test to check if two consecutive getNextTokenNumber return right results
def testToken1():
    token = getNextTokenNumber()
    assert token != None, "token number cannot be None"
    writeToken(token)
    token2 = getNextTokenNumber()
    assert token2 == token+TOKEN_DELTA, "token number is not updated on write"


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


testToken1()
testToken2()