
def findIntersection(gearBox,powerScrew):
    """[Find the Intersection between two line lists]
    
    Arguments:
        line1 {[list of lists]} -- [GearBox X,Y list]
        line2 {[list of lists]} -- [GearBox X,Y list]
    """

    rpmG, torqueG = gearBox[0], gearBox[1]
    rpmP, torqueP = powerScrew[0], powerScrew[1]

    intersectionRPM = 0
    intersectionTorque = 0
    for index in range(0, len(rpmG)): 
        if torqueG[index] <= torqueP[index]:
            intersectionRPM = rpmG[index]
            intersectionTorque = torqueG[index]
            break
    
    return intersectionRPM, intersectionTorque
