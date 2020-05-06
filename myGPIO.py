#import RPi.GPIO as GPIO # import RPi.GPIO module
from myGlobal import myGlobals
import time

#class myGPIOs:

    #def __init__(self):
    #    pass
    
#Raspberry GPIO Config
def funcConfigGPIO():
    if not myGlobals.NORASPBERRY: 
        GPIO.setmode(GPIO.BCM)    # set board mode to Broadcom
        GPIO.setup(15, GPIO.OUT)  # set up pin 15 (Door Open)
        GPIO.setup(16, GPIO.OUT)  # set up pin 17 (Light Tower A)
        GPIO.setup(17, GPIO.OUT)  # set up pin 17 (Light Tower C1)
        GPIO.setup(18, GPIO.OUT)  # set up pin 18 (Led Light)
        GPIO.setup(2, GPIO.IN)    # set up pin 3 (Door CH1)
        GPIO.setup(3, GPIO.IN)    # set up pin 5 (Door CH2)
        GPIO.setup(4, GPIO.IN)    # set up pin 7 (Door Closed)
    else:
        pass
            

#clean up gpio
def funcCleanGPIO():
    if not myGlobals.NORASPBERRY:
        GPIO.cleanup()

#input state
def readInput(valor):
    if not myGlobals.NORASPBERRY:
        return GPIO.input(int(valor))
        
#inside ligth toogle
def outputlightToogle():
    if not myGlobals.NORASPBERRY:
        if  GPIO.input(18):
            GPIO.output(18, 0)
            time.sleep(0.2)
        else:
            GPIO.output(18, 1)
            time.sleep(0.2)

#open door
def outputOpenDoor(valor):
    if not myGlobals.NORASPBERRY:
        GPIO.output(15, int(valor))  #set pin 15 ("Open Door")
        myGlobals.flag_DoorOpen = True
        time.sleep(0.2)         

#set buzzer func
def outputBuzzer(valor):
    if not myGlobals.NORASPBERRY:
        GPIO.output(16,int(valor)) #buzzer
        time.sleep(0.2)
        
#set red light func
def outputAlarmLight (valor):
    if not myGlobals.NORASPBERRY:
        GPIO.output(17,int(valor)) #red light
        time.sleep(0.2)

