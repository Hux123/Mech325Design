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