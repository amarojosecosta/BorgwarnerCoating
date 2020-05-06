import utils

class myGlobals:

    #def __init__(self):
    #    pass

    #Config Variables:
    NOBLABEL = True     #FLAG: A data não está definida na label do coating
    NORASPBERRY = True  #FLAG: prog não compilado no raspberry pi
            
    #messages
    #[lvl, message, state, language]
    arrInfoMsg = [[1,"Porta Aberta!",False,"pt"],   #Porta Aberta
    [5,"Validade Expirada!",False,"pt"],            #Validade expirada
    [6,"Scanner Não Encontrado!",False,"pt"],            #Scanner not found
    [10,"Inserir Dados do Produto..",False,"pt"],    #Dados por inserir
    [15,"Leitura Não Efetudada..",False,"pt"],       #Má leitura do scanner
    [20,"LastInput",False,"pt"],                       #registo da ultima leitura
    [25,"",False,"pt"],
    ]

    #configutation
    gSuperPwd = "9999"
    gPlantName = ""
    gLineName = ""
    gScannerId = ""
    gBCminSize = 9
    gBCmaxSize = 18
    gAlarmTime = ""

    #data control:
    flag_DoorOpen = False           #using
    flag_PortConnected = False   #using
    flag_SupervisorMode = False     #using
    flag_EditMode = False           #using
    flag_BCValid = False            #using
    flag_ProdExpired = False        #using
    flag_ExpDateSelected = False
    flag_ValidValues = False        #using
    flag_ValuesStored = False
    flag_ProductionMode = False

    
    ProdCode = " -"
    ExpDate = " -"
    LastInput = ""

    gNowDate = ""
    gSelDate = ""
    
#clear stored values
def funcClearValues():
    myGlobals.ProdCode = " -"
    myGlobals.ExpDate = " -"
    myGlobals.LastInput = " -"
    myGlobals.flag_BCValid = False
    myGlobals.flag_ProdExpired = False
    myGlobals.flag_ValidValues = False
    myGlobals.flag_ValuesStored = False
    myGlobals.flag_ProductionMode = False

#validate inserted values
def funcValidateBC(valor):
    bcsize = len(valor)
    if (bcsize > int(myGlobals.gBCminSize)) and (bcsize < int(myGlobals.gBCmaxSize)):
        myGlobals.flag_BCValid = True
        return True
    else:
        myGlobals.flag_BCValid = False
        return False

#validate inserted values
def funcValidateDate(valor):
    if myGlobals.ExpDate != " -":
        myGlobals.flag_DateValid = True
    else:
        myGlobals.flag_DateValid = False

#enable data edit
def funcEditData():
    myGlobals.flag_EditMode = True
    myGlobals.flag_ValidValues = False
    myGlobals.flag_BCValid = False
    myGlobals.flag_DateValid = False

#login supervisor mode
def funcSuperviorMode(valor):
    if valor != "":
        if valor == myGlobals.gSuperPwd:
            myGlobals.flag_SupervisorMode = True
        else:
            myGlobals.flag_SupervisorMode = False
    else:
        myGlobals.flag_SupervisorMode = False
  


    
    
    