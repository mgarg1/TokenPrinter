import context

from datetime import datetime
from textToImage import textToImage
import os,sys

BASELINE_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),'baseLine_textToImage.png'))

def compareImageWithBaseline():
    outFile='outFile.png'
    textToImage(tokenNum=23,dateVal='32-Dec-0019',timeVal='25:25:61',outFile=outFile)
    with open(BASELINE_FILE, 'rb') as f, open(outFile, 'rb') as f2:
        c1=f.read()
        c2=f2.read()
        assert c1 == c2, 'generated file doesn\'t match static baseline'
    os.remove(outFile)

compareImageWithBaseline()