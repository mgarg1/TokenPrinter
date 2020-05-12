from datetime import datetime
import os
from eeprom import readString,writeString

TOKEN_START = 12
TOKEN_DELTA = 2
DATE_FORMAT = "%d-%b-%Y"
DATE_START_ADDR = 0
DATE_STR_LENGTH = 11
TOKEN_START_ADDR = 12
TOKEN_STR_LENGTH = 5

def writeToken(tokenNum,lastDay=datetime.now().strftime(DATE_FORMAT).strip()):
    writeString(DATE_START_ADDR,lastDay)
    tokenNumStr = str(tokenNum)
    tokenNumStr = tokenNumStr.zfill(TOKEN_STR_LENGTH)
    writeString(TOKEN_START_ADDR,tokenNumStr)

def readToken():
    lastDay = readString(DATE_START_ADDR, DATE_STR_LENGTH)
    lastToken = readString(TOKEN_START_ADDR, TOKEN_STR_LENGTH) 

    return lastDay,lastToken


def getNextTokenNumber(curr_day=None):
    lastDay,lastToken = readToken()

    if not curr_day:
        curr_day = datetime.now().strftime(DATE_FORMAT).strip()

    #print('lastDay is ' + lastDay)
    if lastDay == curr_day:
        curr_Token = int(lastToken) + TOKEN_DELTA
    else:
        curr_Token = TOKEN_START

    return curr_Token

#writeToken(12)
#a,b = readToken()
#print(a)
#print(b)
