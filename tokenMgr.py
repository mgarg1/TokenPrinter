from datetime import datetime
import os

TOKEN_START = 12
TOKEN_DELTA = 2
LAST_TOKEN_FILENAME = "lastToken.txt"
LAST_DATE_FILENAME = "lastDate.txt"
DATE_FORMAT = "%d-%b-%Y"


def _readFile(filename):
    fileContent=None
    # TODO : if file exist then read
    if os.path.exists(filename):
        with open(filename,'rt') as fileh:
            fileContent = fileh.read().strip()

    return fileContent

def _writeFile(filename,fileContent):
    # filemode is 'w' -> if exist then truncate, otherwise create
     with open(filename,'wt') as fileh:
        fileh.write(fileContent)

def writeToken(tokenNum,lastDay=datetime.now().strftime(DATE_FORMAT).strip()):
    _writeFile(LAST_TOKEN_FILENAME,str(tokenNum))
    _writeFile(LAST_DATE_FILENAME,lastDay)

def getNextTokenNumber(curr_day=None):
    lastDay = _readFile(LAST_DATE_FILENAME)
    lastToken = _readFile(LAST_TOKEN_FILENAME)

    if not curr_day:
        curr_day = datetime.now().strftime(DATE_FORMAT).strip()
    
    if lastDay == curr_day:
        curr_Token = int(lastToken) + TOKEN_DELTA
    else:
        curr_Token = TOKEN_START

    return curr_Token

