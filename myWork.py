from PyQt5.QtCore import QThread, pyqtSignal, QObject, QDate
import time
import utils
import sys
import os
from usbRead import UsbBarCodeReader
import datetime
import myGlobal
import myGPIO
from myGlobal import myGlobals 

class myThread (QThread, QObject):
 
    siglabel_1 = pyqtSignal(str)    #Product Code
    siglabel_2 = pyqtSignal(str)    #Expiry Date
    siglabel_3 = pyqtSignal(str)    #Info Message
    siglabel_4 = pyqtSignal(str)    #Date label
    siglabel_5 = pyqtSignal(str)    #Scanner status label

    sigbutton_1 = pyqtSignal(bool)  #Alarm button: true = show; false = hide
    sigbutton_2 = pyqtSignal(bool)  #Store Prod button: true = enable; false = disable

    def __init__(self, parent=None):
        QThread.__init__(self, parent)  #inicializar thread

        #INSTANCES
        self.usb = UsbBarCodeReader()   #USB Scanner

        #RPI GPIO CONFIG
        myGPIO.funcConfigGPIO()     #config GPIO
        myGPIO.outputOpenDoor(0)    #close door
        myGPIO.outputBuzzer(0)      #buzzer off
        myGPIO.outputAlarmLight(0) #red light off
        #myGPIO.funcCleanGPIO()     #clear GPIO
        #SCANNER CONECTION 
        self.scannerPort = self.usb.findUsbPort(myGlobals.gScannerId)   #find usb scanner port
        if self.scannerPort != "":
            myGlobals.flag_PortConnected = self.usb.openPort(self.scannerPort, 0.3)  #open usb scanner port
        else:
            #myGlobals.arrInfoMsg[2][2] = True
            myGlobals.flag_PortConnected = False

    #set buzzer & ligth
    def setAlarm(self):
        #myGlobals.arrInfoMsg[1][2] = True
        self.sigbutton_1.emit(True)    #show 'reset alarm' button
        myGPIO.outputBuzzer(1)    #set alarm buzzer
        myGPIO.outputAlarmLight(1)#set alarm light
    
    #reset buzzer & ligth
    def rstAlarm(self):
        myGPIO.outputBuzzer(0)    #reset buzzer
        myGPIO.outputAlarmLight(0)#reset alarm light
        myGlobal.funcClearValues()
        self.sigbutton_1.emit(False)

    #Alarm Information
    #def checkError(self):
     #   msg = ""
      #  for x in range(len(myGlobals.arrInfoMsg)):
       #     if myGlobals.arrInfoMsg[x][2]:  #Alarm on
        #        msg = myGlobals.arrInfoMsg[x][1]
                #self.siglabel_3.emit(msg)
      

    #Main cicle
    def run(self):
        #Machine cicle
        while True:
            #Print real time
            nowDate = datetime.datetime.now()
            nowDate = nowDate.strftime("%d/%m/%Y")
            self.siglabel_4.emit(nowDate)
            #============================
            #    MACHINE ROUTINES
            #============================
            #check if door open -> reset output signal
            #input_4 (Door_Closed) when door aberto = 1
            if myGlobals.flag_DoorOpen:
                if myGPIO.readInput(4):   #door opened
                    time.sleep(1)
                    myGlobals.flag_DoorOpen = False
                    myGPIO.outputOpenDoor(0)
                    
            #============================
            #    MACHINE INFORMATION
            #============================
            #check for Error
            #self.checkError()
            
            #CHECK VALUES:
            if myGlobals.flag_BCValid and myGlobals.flag_DateValid:
                myGlobals.flag_ValidValues = True
            else:
                myGlobals.flag_ValidValues = False
           
            #============================
            #       CHECK IF DATE VALID
            #============================
            if myGlobals.flag_ExpDateSelected or myGlobals.flag_ProductionMode:
                nowDate = myGlobals.gNowDate
                selDate = myGlobals.gSelDate
                myGlobals.flag_ExpDateSelected = False
                self.siglabel_2.emit(myGlobals.gSelDate)     
                try:
                    if selDate[6:] > nowDate[6:]:           #check year
                        myGlobals.flag_ProdExpired = False 
                    if selDate[6:] < nowDate[6:]:
                        myGlobals.flag_ProdExpired = True
                    if selDate[6:] == nowDate[6:]:   
                        if selDate[3:5] > nowDate[3:5]:     #check month
                            myGlobals.flag_ProdExpired = False
                        if selDate[3:5] < nowDate[3:5]:
                            myGlobals.flag_ProdExpired = True
                        if selDate[3:5] == nowDate[3:5]:    
                            if selDate[:2] <= nowDate[:2]:  #check day
                                myGlobals.flag_ProdExpired = True
                            if selDate[:2] > nowDate[:2]:
                                myGlobals.flag_ProdExpired = False
                    if myGlobals.flag_ProdExpired:          #print result                       
                        self.siglabel_3.emit("Product Expired!")
                    else:
                        self.siglabel_3.emit("Product Date Is Valid!") 
                except:
                    pass
            
                if myGlobals.flag_ProdExpired:
                    nowTime = datetime.datetime.now()   #define time to trigger alarm
                    Time = nowTime.strftime("%H:%M")
                    if Time >= myGlobals.gAlarmTime:
                        self.setAlarm()                    
                else:
                    self.rstAlarm()
            
            #============================
            #       CHECK DATA IS VALID
            #============================
            #clear data information
            if myGlobals.flag_EditMode:
                if myGlobals.flag_BCValid and myGlobals.flag_DateValid:
                    myGlobals.flag_ValidValues = True
                else:
                    myGlobals.flag_ValidValues = False

            #============================
            #       SCANNER
            #============================
            #scanner connection status
            if myGlobals.flag_PortConnected:
                self.siglabel_5.emit("Connected!")
            else:
                self.siglabel_5.emit("Not connected!")
            #scanner reading
            self.result, self.scannerStatus = self.usb.readAllWithTerminator('\r')
            time.sleep (0.2)
            myGlobals.flag_PortConnected = self.scannerStatus
            if self.scannerStatus:                                                      #connected
                if self.result != "" and self.scannerStatus == True:
                    self.result = self.result[0:len(self.result)]
                    if myGlobals.flag_EditMode:                           #if in 'edit mode'
                        self.value = myGlobal.funcValidateBC(self.result)          #check if scanned result is valid 
                        if self.value:       #bc result valid                                           #if result 'valid'
                            myGlobals.ProdCode = self.result           #save result
                            self.siglabel_1.emit(myGlobals.ProdCode)   #print result
                            time.sleep (0.2)
                else:
                    pass
            else:                                                                               #not connected                
                self.scannerPort = self.usb.findUsbPort(myGlobals.gScannerId)   #find usb scanner port
                time.sleep(0.2)
                if self.scannerPort != "":
                    self.portResult = self.usb.openPort(self.scannerPort, 0.3)                  #open usb scanner port

            


            