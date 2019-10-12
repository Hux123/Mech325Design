# Conversion of units
def ItoSIVelocity(I): 
    return(0.00508*I)
    
def SItoIVelocity(SI):
    return(196.85*SI)

def cmtoinch(cm):
    return(cm*0.393701)

def inchtocm(inch):
    return(inch*2.54)
    
def ItoSIForce(I):
    return(I*4.44822) 
    
def SItoIForce(SI):
    return(SI*0.224809)

def inchToFeet(inch):
    return inch / 12

def newtonToPound(newton):
    return newton * 0.224809

def torqueNmToPoundFeet(torqueNm):
    return torqueNm * 0.737562

def torquePoundFeetToNm(torquePoundFeet):
    return torquePoundFeet /  0.737562