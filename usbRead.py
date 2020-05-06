import serial
import serial.tools.list_ports as prtlst
import time

class UsbBarCodeReader:

    def __init__(self):
        pass    #para uso futuro
        #self.port = port
        #self.portTimeout = portTimeout

    def findUsbPort(self, id):      #returns dev port
        self.id = id                #dev model
        pts= prtlst.comports()
        for pt in pts:
            if self.id in pt[1]:    #pt[1] devs names
                return pt[0]        #pt[0] devs port
        return ""

    def openPort(self, port, portTimeout):
        self.port = port
        self.portTimeout = portTimeout
        try:
            self.ser = serial.Serial(self.port, self.portTimeout)
            self.ser.flush()
            return True
        except: return False
            
    def closePort(self):
        try:
            self.port.close()
        except: 
            print("not closed")
            pass

    def readOnechar(self):
        try:
            data = self.ser.readOnechar()
            return data.decode('utf-8'), True
        except: return '', False

    def readLine(self):
        try:
            line = self.ser.readline()
            return line.decode('utf-8'), True
        except: return '', False

    def readAll(self):
        try:
            allBytes = self.ser.read_all()
            return allBytes.decode('utf-8'), True
        except: return '', False

    def readAllWithTerminator(self, terminator):
        self.terminator = terminator
        try:
            allBytes = self.ser.read_all().decode('utf-8')
            if allBytes == '':                  #no code was read
                return '', True 

            if allBytes[-1] == self.terminator: #read code with terminator
                return allBytes[0:-1], True
            else:                               #read code with no terminator (result could be bigger than buffer)
                time.sleep(0.1)
                someBytes = self.ser.read_all().decode('utf-8') #read again
                if someBytes == '':
                    return '', False            #result no valid
                
                if someBytes[-1] == self.terminator:
                    return allBytes + someBytes[0:-1], True #read code with terminator
                else:   
                    return '', False            #read code with no terminator

        except: return '', False                #invalid reading, disconnected

    def readUntil(self, untilChar):
        self.untilChar = untilChar
        try:
            line = self.ser.read_until(self.untilChar.encode())
            line = line.decode('utf-8')
            return line[0:len(line)-1], True
        except: return '', False