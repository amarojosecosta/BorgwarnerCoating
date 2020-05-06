import xml.dom.minidom as xmldoc
from xml.etree.ElementTree import ElementTree
import os
import datetime
import time

class Variables:
    plantName = ''
    lineName = ''
    prodCode = ''
    scannerId = ''
    bcMinSize = ''
    bcMaxSize = ''

def readConfigFile (filename):
    try:
        tree = ElementTree()
        root = tree.parse(filename)
         
        node = root.find("plantName")
        Variables.plantName = node.text
        node = root.find("prodLine")
        Variables.lineName = node.text
        node = root.find("prodCode")
        Variables.prodCode = node.text
        node = root.find("scannerId")
        Variables.scannerId = node.text
        node = root.find("bcMinSize")
        Variables.bcMinSize = node.text
        node = root.find("bcMaxSize")
        Variables.bcMaxSize = node.text
        node = root.find("AlarmTime")
        Variables.AlarmTime = node.text

        return True
    except:
        writeLogFile ('Error reading configuration file')
        return False

def writeLogFile (text):
    try:
        appPath = os.path.dirname(os.path.abspath(__file__))
        filename = appPath + '/log.txt'
        dt = datetime.datetime.now().strftime('%Y:%m:%d %H:%M:%S')
        if (os.path.isfile(filename)):
            if os.stat(filename).st_size >  32000: f = open(filename, 'w')
            else: f = open(filename, 'a')
        else:
            f = open(filename, 'w')
        f.write (dt + ' - ' + text + '\n')
        f.close()
    except:
        'No log will be written'

