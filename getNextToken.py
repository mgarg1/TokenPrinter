import time
from datetime import datetime

SW1 = 8
LED1 = 10
LED2 = 12

TOKEN_START = 12
TOKEN_DELTA = 2
LAST_TOKEN_FILENAME = "lastToken.txt"
LAST_DATE_FILENAME = "lastDate.txt"

def setupFiles(filename):
    with open(filename,'a',encoding = 'utf-8') as f:
        pass

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

def getNextTokenNumber(filename=LAST_DATE_FILENAME):
    with open(filename,'r+',encoding = 'utf-8') as dateFile:
     
        content = dateFile.read()
        date = content.split()[0]
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