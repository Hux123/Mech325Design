
def findIntersection(gearBox, powerScrew, motorInput):
    """[Find the Intersection between two line lists]
    
    Arguments:
        line1 {[list of lists]} -- [GearBox X,Y list]
        line2 {[list of lists]} -- [GearBox X,Y list]
    """

    rpmG, torqueG = gearBox[0], gearBox[1]
    rpmP, torqueP = powerScrew[0], powerScrew[1]
    rpmM, torqueM = motorInput[0],motorInput[1]


    startIndexG = 0
    for i in range(0, len(rpmG)):
        if torqueG[i] != 0 :
            startIndexG = i
            break
    
    startRPMG = rpmG[startIndexG]
    startTorqueG = torqueG[startIndexG]

    endIndexG = len(rpmG) - 1
    i = len(rpmG) - 1
    while i > 0:
        if torqueG[i] != 0 :
            endIndexG = i
            break
        i -= 1
        
    endRPMG = rpmG[endIndexG]
    endTorqueG = torqueG[endIndexG]

    slopeG = (endTorqueG - startTorqueG) / (endRPMG - startRPMG)

    startRPMG = int(startRPMG)
    endRPMG = int(endRPMG)

    torqueG = []
    rpmG = []
    for omega in range(startRPMG, endRPMG + 1):
        torque = slopeG * (omega - startRPMG) + startTorqueG
        torqueG.append(torque)
        rpmG.append(omega)


    intersectionRPM = 0
    intersectionTorque = 0
    motorInputRPM = 0
    motorInputTorque = 0
    for index in range(0, len(rpmG) - 1):
        if torqueG[index] >= torqueP[index] and torqueG[index + 1] <= torqueP[index + 1]:
            intersectionRPM = rpmG[index]
            intersectionTorque = torqueG[index]
            motorInputRPM = rpmM[index]
            motorInputTorque = torqueM[index]
            break
            


    
    return intersectionRPM, intersectionTorque, motorInputRPM, motorInputTorque
