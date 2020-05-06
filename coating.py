from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSlot, QDate
#from design import Ui_MainWindow  # importing our ui generated file
from MainWindow import Ui_MainWindow
from myWork import myThread
import sys, os
import utils
import datetime
import calendar
from myGlobal import myGlobals
import myGlobal
import myGPIO

class mywindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(mywindow, self).__init__()
        #INSTANCES
        self.ui = Ui_MainWindow()   # gui object
        self.ui.setupUi(self)
        self.show()
        #self.showMaximized()
        self.showFullScreen()

        #read .xml    
        if not utils.readConfigFile('config.xml'):
            self.closeApp()
        else:
            myGlobals.gPlantName = utils.Variables.plantName    #Plant name
            myGlobals.gLineName = utils.Variables.lineName      #Prdution line id
            myGlobals.gScannerId = utils.Variables.scannerId    #Scanner model id
            myGlobals.gBCminSize = utils.Variables.bcMinSize    #Barcode min len size
            myGlobals.gBCmaxSize = utils.Variables.bcMaxSize    #Barcode max len size
            myGlobals.gAlarmTime = utils.Variables.AlarmTime

        #inicialize ui objets
        self.ui.btnAlarmRst.hide()                      #Hide Alarm button
        self.ui.btnStoreProd.setText("EDIT DATA")       #
        self.ui.btnStoreProd.setEnabled(False)          #disable 'edit data' button
        self.ui.btnDoor.setEnabled(False)               #disable 'open door' button
        self.ui.btnExit.setEnabled(False)               #disable 'exit' button
        self.ui.dateEdit.setEnabled(False)              #disable 'date edit' calendar
        self.ui.dateEdit.setMinimumDate(QtCore.QDate.currentDate()) #set current date
        self.ui.lineeditPwdEntry.setEchoMode(self.ui.lineeditPwdEntry.Password)
        self.ui.lblExpDate.setText(myGlobals.ExpDate)   #init 'expiration date' label
        self.ui.lblProdCode.setText(myGlobals.ProdCode) #init 'prod code' label
        self.ui.lblInfo.setText(" -")                   #init 'info' label
        self.ui.lbldate.setText(" -")                   #init 'atual date' label
        self.ui.lblLineCompanyId.setText(myGlobals.gPlantName +
         ": " + myGlobals.gLineName)
    
        #THREAD INSTANCE
        self.threadClass = myThread()
        
        #SIGNALS
        #labels
        self.threadClass.siglabel_1.connect(self.updatelabel_1) #ProductCode label
        self.threadClass.siglabel_2.connect(self.updatelabel_2) #ExpirationDate label
        self.threadClass.siglabel_3.connect(self.updatelabel_3) #Information Label
        self.threadClass.siglabel_4.connect(self.updatelabel_4) #Date label
        self.threadClass.siglabel_5.connect(self.updatelabel_5) #Scanner Status label
        #buttons
        self.threadClass.sigbutton_1.connect(self.updatebutton_1)
        #buttons events
        self.ui.btnDoor.clicked.connect(self.on_click_1)        #Open door button
        self.ui.btnLight.clicked.connect(self.on_click_2)       #Turn light button
        self.ui.btnExit.clicked.connect(self.on_click_3)        #Close app button
        self.ui.btnAlarmRst.clicked.connect(self.on_click_4)    #Reset Alarm button
        self.ui.btnStoreProd.clicked.connect(self.on_click_5)   #edit/store data button
        self.ui.btnLogin.clicked.connect(self.on_click_6)
        #dataedit event
        self.ui.dateEdit.dateChanged.connect(self.onDateChanged)
        
    
        #start thread
        self.threadClass.start()

    #========================================================
    #SIGNALS SLOTS - FROM THREAD
    #LABELS
    @pyqtSlot(str)  #ProdCode lbl
    def updatelabel_1(self, valor):
        self.ui.lblProdCode.setText(valor)
    
    @pyqtSlot(str)  #ExpDate lbl
    def updatelabel_2(self, valor):
        self.ui.lblExpDate.setText(valor)
    
    @pyqtSlot(str)  #Info lbl
    def updatelabel_3(self, valor):
        self.valor = valor
        self.ui.lblInfo.setText(valor)
    
    @pyqtSlot(str)  #Atual date lbl
    def updatelabel_4(self, valor):
        self.ui.lbldate.setText(valor)

    @pyqtSlot(str)  #Scanner status lbl
    def updatelabel_5(self, valor):
        self.ui.lblScannerStatus.setText(valor)
        if valor == "Connected!":
            self.ui.lblScannerStatus.setStyleSheet('color: green')
        else:
            self.ui.lblScannerStatus.setStyleSheet('color: red')
    
    #Buttons state managment
    @pyqtSlot(bool) #Update 'Reset Alarm' btn
    def updatebutton_1(self, valor):
        if bool(valor):
            self.ui.btnAlarmRst.show()
            self.ui.btnAlarmRst.setEnabled(True)
        else: 
            self.ui.btnAlarmRst.hide()
            self.ui.btnAlarmRst.setEnabled(False)

    #===============================================
    #BUTTONS SIGNALS FROM UI
    @pyqtSlot() #Open Door
    def on_click_1(self):
        myGPIO.outputOpenDoor(1)
        
    @pyqtSlot() #Turn light
    def on_click_2(self):
        myGPIO.outputlightToogle()
    
    @pyqtSlot() #Close app
    def on_click_3(self):
        self.closeApp()
    
    @pyqtSlot() #Reset Alarm
    def on_click_4(self):
        myGlobals.flag_ProdExpired = False
        myGPIO.outputBuzzer(0)      #reset buzzer
        myGPIO.outputAlarmLight(0)  #reset alarm light
    
    @pyqtSlot() #Edit/Store data button
    def on_click_5(self): 
        if not myGlobals.flag_EditMode:             #EDIT TASKS
            #in edit mode:
            self.ui.dateEdit.setEnabled(True)                
            self.ui.btnStoreProd.setText("STORE DATA")
            #functions(clear/enable data change):
            myGlobals.flag_ProductionMode = False
            myGlobal.funcEditData()                
            myGlobal.funcClearValues()
            self.ui.lblProdCode.setText(myGlobals.ProdCode)
            self.ui.lblExpDate.setText(myGlobals.ExpDate)             
        if myGlobals.flag_EditMode:                 #STORE TASKS
            self.valid1 = myGlobals.flag_BCValid
            self.valid2 = myGlobals.flag_ProdExpired
            if (self.valid1 and not (self.valid2)): #IF VALUES VALID
                self.ui.btnStoreProd.setText("EDIT DATA")
                self.ui.btnStoreProd.setEnabled(False)
                self.ui.dateEdit.setEnabled(False)
                self.ui.btnDoor.setEnabled(False)
                self.ui.btnExit.setEnabled(False)
                myGlobals.flag_ValidValues = True
                myGlobals.flag_ProductionMode = True
                myGlobals.flag_EditMode = False
                myGlobals.flag_SupervisorMode = False
                self.ui.btnLogin.setText("SUPERVISOR")
            else:                                   #VALUES NOT VALID
                self.ui.btnStoreProd.setText("STORE DATA")
                myGlobals.flag_ValidValues = False
            '''
                #NOT VALID MESSAGE!
            '''
    
    @pyqtSlot() #supervisor button
    def on_click_6(self):       
        if not (myGlobals.flag_SupervisorMode):               #IF IN USER MODE
            #login
            self.pwd = self.ui.lineeditPwdEntry.text()      
            myGlobal.funcSuperviorMode(self.pwd)
            if myGlobals.flag_SupervisorMode:               #CORRECT PWD
                #update ui for supervisor user
                self.ui.btnStoreProd.setEnabled(True)
                self.ui.btnStoreProd.setText("EDIT MODE")       
                self.ui.btnDoor.setEnabled(True)            
                self.ui.btnExit.setEnabled(True)            
                self.ui.btnLogin.setText("LOGOUT")
                self.ui.lineeditPwdEntry.clear() 
                self.ui.lblInfo.setText("On Supervisor Mode!")               
            else:                                           #WRONG PWD
                self.ui.lineeditPwdEntry.clear()            
        else:                                               #IF IN SUPERVISOR MODE                             
            #logout
            myGlobals.flag_SupervisorMode = False            
            myGlobals.flag_EditMode = False
            #update ui for normal user
            self.ui.btnLogin.setText("SUPERVISOR")
            self.ui.btnStoreProd.setEnabled(False)
            self.ui.btnStoreProd.setText("EDIT DATA")                   
            self.ui.btnDoor.setEnabled(False)            
            self.ui.btnExit.setEnabled(False)
            self.ui.btnAlarmRst.setEnabled(False)
            self.ui.dateEdit.setEnabled(False)
            if not (myGlobals.flag_ValuesStored):
                #clear values if not stored
                myGlobal.funcClearValues()
                self.ui.lblProdCode.setText(str(myGlobals.ProdCode))
                self.ui.lblExpDate.setText(str(myGlobals.ExpDate))
                self.ui.lblInfo.setText("Data Wasn't Stored!")
                   

    @pyqtSlot() #Expire date
    def onDateChanged(self):
        #selected date
        tempSelDate = self.ui.dateEdit.date()           
        tempSelDate = tempSelDate.toPyDate()            
        lselDate = tempSelDate.strftime("%d/%m/%Y")     
        myGlobals.gSelDate = lselDate
        #actual date
        lnowDate = datetime.datetime.now()
        lnowDate = lnowDate.strftime("%d/%m/%Y")
        myGlobals.gNowDate = lnowDate
        #set flag
        myGlobals.flag_ExpDateSelected = True
        
    def closeApp(self):
        myGPIO.outputBuzzer(0)      #buzzer off
        myGPIO.outputAlarmLight(0) #red light off
        sys.exit(app.exec_())
        pass  # o que quiser fazer

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = mywindow()
    """ application é uma instancia d
    a classe mywindow onde está definido o objecto ui que por
    vez é uma instância da classe UI_Form onde está inicializado o form (objectos gráficos) """
    application.show()
    sys.exit(app.exec_())
