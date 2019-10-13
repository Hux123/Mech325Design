#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[60]:


import math

# Pitch Diameter
# Face Width
# Torque, Speed
# Quality Factor
# Brinell Hardness
# Need to get Lewis form factor from tooth number in textbook
# Need stress cycle factor from table in textbook which depends on material
# Need to get J from figure 14-6 in the book (Bending strength geometry factor)
# Need allowable stresses depndent on the gears selected

overloadFactor = 1.25
reliabilityFactor = 1.25
pressureAngle = 20
qualityFactor = 5
estimatedCycles = 500 * 4*10**4 #estimated with the given pitch of the power screww and biggest difference in gear diameter
bendingStressCycleFactor = 1.3558 * estimatedCycles**-0.0178
pittingStressCycleFactor =  1.4488 * estimatedCycles ** -0.023


def getFishRatio(material):
    if material == 1020:
        return 0.29
    if material == 1117:
        return 0.28
    if material == 1144:
        return 0.28

def getBrinellHardness(material):
    if material == 1020:
        return 137
    if material == 1117:
        return 120
    if material == 1144:
        return 217
    
def getElasticModulus(material):
    if material == 1020:
        return 29000
    else:
        return 28000

def getDynamicFactor(qualityFactor, tangentialSpeed):
    B = 0.25 * (12 - qualityFactor) ** (2/3)
    A = 50 + 56 * (1 - B)
    return ((A + tangentialSpeed **0.5)/A)**B

def getAllowableBendingStress(hardness):
    return 77.3 * hardness + 12800

def getAllowableContactStress(hardness):
    return 82.3 * hardness + 12150

def getSizeFactor(diametralPitch, lewisFormFactor, faceWidth):
    return 1.192 * (faceWidth * lewisFormFactor **0.5 / diametralPitch)**0.0535

def getLoadDistributionFactor(faceWidth, pinionPitch, qualityNumber):
    cmc = 1
    cpf = (faceWidth / (10 * pinionPitch) - 0.025) if faceWidth > 1 else faceWidth / (10 * pinionPitch) - 0.0375 + 0.0125 * faceWidth
    cpm = 1.1
    cma = 0.247**2 + 0.0167 * (faceWidth) - 0.0000765 * (faceWidth)**2
    ce = 1
    return 1 + cmc * (cpf * cpm + cma * ce)

def getGeometryFactorPittingResistance(gearRatio):
    return math.cos(pressureAngle*math.pi/180) * math.sin(pressureAngle*math.pi/180) / 2 * gearRatio/(gearRatio + 1)

def getElasticCoefficient(pinionPoisson, pinionYoungsModulus, gearPoisson, gearYoungsModulus):
    return (1 / (math.pi * ((1 - pinionPoisson ** 2) / pinionYoungsModulus + (1 - gearPoisson ** 2) / gearYoungsModulus))) ** 0.5

def getHardnessRatioFactor(isPinion, pinionHardness, gearHardness, gearRatio):
    if isPinion:
        return 1
    else:
        aFactor = 8.98*10**-3 * pinionHardness/gearHardness - 8.29*10**-3
        return 1 + aFactor * (gearRatio - 1)

def getBendingStress(tangentialForce, dynamicFactor, sizeFactor, diametralPitch, faceWidth, loadDistributionFactor, bendingGeometryFactor):
    return tangentialForce * overloadFactor * dynamicFactor * sizeFactor * diametralPitch * loadDistributionFactor / (faceWidth * bendingGeometryFactor)

def getBendingFactorOfSafety(allowableStress, bendingStress, reliabilityFactor, stressCycleFactor):
    return allowableStress * stressCycleFactor / reliabilityFactor / bendingStress

def getContactStress(elasticCoefficient, tangentialForce, dynamicFactor, sizeFactor, loadDistributionFactor, pinionDiameter, faceWidth, bendingGeometryFactor):
    return elasticCoefficient * (tangentialForce * overloadFactor * dynamicFactor * sizeFactor * loadDistributionFactor / (pinionDiameter * faceWidth * bendingGeometryFactor))**0.5

def getContactFactorOfSafety(allowableContactStress, stressCycleFactor, contactStress, hardnessRatioFactor, reliabilityFactor):
    return allowableContactStress * stressCycleFactor * hardnessRatioFactor / reliabilityFactor / contactStress

def checkStresses(requiredFactorOfSafety, tangentialSpeed, tangentialForce, material, diametralPitch, faceWidth, pinionTeeth, gearTeeth, pLewisFormFactor, gLewisFormFactor, pBendingGeometryFactor, gBendingGeometryFactor):
    pYoungModulus = getElasticModulus(material)
    pPoisson = getFishRatio(material)
    pHardness = getBrinellHardness(material)
    gYoungModulus = getElasticModulus(material)
    gPoisson = getFishRatio(material)
    gHardness = getBrinellHardness(material)
    
    pAllowableBendingStress = getAllowableBendingStress(pHardness)
    pAllowableContactStress = getAllowableContactStress(pHardness)
    gAllowableBendingStress = getAllowableBendingStress(gHardness)
    gAllowableContactStress = getAllowableContactStress(gHardness)
    
    pDynamicFactor = getDynamicFactor(qualityFactor, tangentialSpeed)
    gDynamicFactor = getDynamicFactor(qualityFactor, tangentialSpeed)
    pSizeFactor = getSizeFactor(diametralPitch, pLewisFormFactor, faceWidth)
    gSizeFactor = getSizeFactor(diametralPitch, gLewisFormFactor, faceWidth)
    loadDistributionFactor = getLoadDistributionFactor(faceWidth, pinionTeeth/diametralPitch, qualityFactor)
    geometryFactorPittingResistance = getGeometryFactorPittingResistance(gearTeeth/pinionTeeth)
    elasticCoefficient = getElasticCoefficient(pPoisson, pYoungModulus, gPoisson, gYoungModulus)
    pHardnessRatioFactor = getHardnessRatioFactor(True, pHardness, gHardness, gearTeeth/pinionTeeth)
    gHardnessRatioFactor = getHardnessRatioFactor(False, pHardness, gHardness, gearTeeth/pinionTeeth)    
    pBendingStress = getBendingStress(tangentialForce, pDynamicFactor, pSizeFactor, diametralPitch, faceWidth, loadDistributionFactor, pBendingGeometryFactor)
    gBendingStress = getBendingStress(tangentialForce, gDynamicFactor, gSizeFactor, diametralPitch, faceWidth, loadDistributionFactor, gBendingGeometryFactor)
    pContactStress = getContactStress(elasticCoefficient, tangentialForce, pDynamicFactor, pSizeFactor, loadDistributionFactor, pinionTeeth/diametralPitch, faceWidth, geometryFactorPittingResistance)
    gContactStress = (gSizeFactor / pSizeFactor)**0.5 * pContactStress
    pinionBFOS = getBendingFactorOfSafety(pAllowableBendingStress, pBendingStress, reliabilityFactor, bendingStressCycleFactor)
    gearBFOS = getBendingFactorOfSafety(gAllowableBendingStress, gBendingStress, reliabilityFactor, bendingStressCycleFactor)
    pinionCFOS = getContactFactorOfSafety(pAllowableContactStress, pittingStressCycleFactor, pContactStress, pHardnessRatioFactor, reliabilityFactor)
    gearCFOS = getContactFactorOfSafety(gAllowableContactStress, pittingStressCycleFactor, gContactStress, gHardnessRatioFactor, reliabilityFactor)
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




