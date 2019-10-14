import math

# 

overloadFactor = 1.25
pressureAngle = 20
qualityFactor = 5
reliability = 0.999
estimatedCycles = 500 * 4*10**4 #estimated with the given pitch of the power screw and biggest difference in gear diameter
bendingStressCycleFactor = 1.3558 * estimatedCycles**-0.0178
pittingStressCycleFactor =  1.4488 * estimatedCycles ** -0.023

def getFishRatio(material):
    """[Returns Poission ration for given material]
    
    Arguments:
        material {[int]} -- [Carbon steel type]
    
    Returns:
        [double] -- [Poisson ratio]
    """
    if material == 1020:
        return 0.29
    if material == 1117:
        return 0.28
    if material == 1144:
        return 0.28

def getBrinellHardness(material):
    """[Returns Brinell Hardness for given material]
    
    Arguments:
        material {[int]} -- [Carbon steel type]
    
    Returns:
        [int] -- [Brinell Hardness]
    """
    if material == 1020:
        return 137
    if material == 1117:
        return 120
    if material == 1144:
        return 217
    
def getReliabilityFactor(reliability):
    """[Returns reliability factor]
    
    Arguments:
        material {[double]} -- [Reliability]
    
    Returns:
        [double] -- [Reliability Factor]
    """
    return 0.50-0.109*math.log(1 - reliability)
    
def getElasticModulus(material):
    """[Returns Elastic Modulus for given material]
    
    Arguments:
        material {[int]} -- [Carbon steel type]
    
    Returns:
        [int] -- [Elastic]
    """
    if material == 1020:
        return 29000
    else:
        return 28000

def getDynamicFactor(qualityFactor, tangentialSpeed):
    """[Calculates Dynamic Factor]
    
    Arguments:
        qualityFactor {[int]} -- [Quality factor]
        tangentialSpeed {[double]} -- [Tangential Speed of Gears]
    
    Returns:
        [double] -- [Dynamic Factor]
    """
    B = 0.25 * (12 - qualityFactor) ** (2/3)
    A = 50 + 56 * (1 - B)
    return ((A + tangentialSpeed **0.5)/A)**B

def getAllowableBendingStress(hardness):
    """[Calculates Allowable Bending Stress]
    
    Arguments:
        hardness {[int]} -- [Brinell Hardness]
    
    Returns:
        [double] -- [Allowable Bending Stress]
    """
    return 77.3 * hardness + 12800

def getAllowableContactStress(hardness):
    """[Calculates Allowable Contact Stress]
    
    Arguments:
        hardness {[int]} -- [Brinell Hardness]
    
    Returns:
        [double] -- [Allowable Contact Stress]
    """
    return 82.3 * hardness + 12150

def getSizeFactor(diametralPitch, lewisFormFactor, faceWidth):
    """[Calculates Size Factor]
    
    Arguments:
        diametralPitch {[double]} -- [Diametral Pitch]
        lewisFormFactor {[double]} -- [Lewis Form Factor]
        faceWidth {[double]} -- {Face Width}
    
    Returns:
        [double] -- [Size Factor]
    """
    return 1.192 * (faceWidth * lewisFormFactor **0.5 / diametralPitch)**0.0535

def getLoadDistributionFactor(faceWidth, pinionPitch, qualityNumber):
    """[Calculates Size Factor]
    
    Arguments:
        faceWidth {[double]} -- [Face Width]
        pinionPitch {[double]} -- [Pinion Pitch]
        qualityForm {[double]} -- {Quality Number}
    
    Returns:
        [double] -- [Load Distribution Factor]
    """
    cmc = 1
    cpf = (faceWidth / (10 * pinionPitch) - 0.025) if faceWidth > 1 else faceWidth / (10 * pinionPitch) - 0.0375 + 0.0125 * faceWidth
    cpm = 1.1
    cma = 0.247**2 + 0.0167 * (faceWidth) - 0.0000765 * (faceWidth)**2
    ce = 1
    return 1 + cmc * (cpf * cpm + cma * ce)

def getGeometryFactorPittingResistance(gearRatio):
    """[Calculates Geometry Factor Pitting Resistance]
    
    Arguments:
        gearRatio {[double]} -- [Gear Ratio]
    
    Returns:
        [double] -- [Geometry Factor Pitting Resistance]
    """
    return math.cos(pressureAngle*math.pi/180) * math.sin(pressureAngle*math.pi/180) / 2 * gearRatio/(gearRatio + 1)

def getElasticCoefficient(pinionPoisson, pinionYoungsModulus, gearPoisson, gearYoungsModulus):
    """[Calculates Elastic Coefficient]
    
    Arguments:
        pinionPoisson {[double]} -- [Pinion Poisson Ratio]
        pinionYoungsModulus {[double]} -- [Pinion Young's Modulus]
        gearPoisson {[double]} -- [Gear Poisson Ratio]
        gearYoungsModulus {[double]} -- [Gear Young's Modulus]
    
    Returns:
        [double] -- [Elastic Coefficient]
    """
    return (1 / (math.pi * ((1 - pinionPoisson ** 2) / pinionYoungsModulus + (1 - gearPoisson ** 2) / gearYoungsModulus))) ** 0.5

def getHardnessRatioFactor(isPinion, pinionHardness, gearHardness, gearRatio):
    """[Calculates Hardness Ratio Factor]
    
    Arguments:
        isPinion {[bool]} -- [True if gear is the pinion]
        pinionHardness {[double]} -- [Pinion Hardness]
        gearHardness {[double]} -- [Gear Hardness]
        gearRatio {[double]} -- [Gear Ratio]
    
    Returns:
        [double] -- [Hardness Ratio Factor]
    """
    if isPinion:
        return 1
    else:
        aFactor = 8.98*10**-3 * pinionHardness/gearHardness - 8.29*10**-3
        return 1 + aFactor * (gearRatio - 1)

def getBendingStress(tangentialForce, dynamicFactor, sizeFactor, diametralPitch, faceWidth, loadDistributionFactor, bendingGeometryFactor):
    """[Calculates Bending Stress]
    
    Arguments:
        tangentialForce {[double]} -- [Tangential force]
        dynamicFactor {[double]} -- [Dynamic Factor]
        sizeFactor {[double]} -- [Size Factor]
        diametralPitch {[double]} -- [Diametral Pitch]
        faceWidth {[double]} -- [faceWidth]
        loadDistributionFactor{[double]} -- [Load Distribution Factor]
        bendingGeometryFactor{[double]} -- [Bending Geometry Factor]
    
    Returns:
        [double] -- [Bending Stress]
    """
    return tangentialForce * overloadFactor * dynamicFactor * sizeFactor * diametralPitch * loadDistributionFactor / (faceWidth * bendingGeometryFactor)

def getBendingFactorOfSafety(allowableStress, bendingStress, reliabilityFactor, stressCycleFactor):
    """[Calculates Bending Factor of Safety]
    
    Arguments:
        allowableStress {[double]} -- [Allowable stress]
        bendingStress {[double]} -- [Bending stress]
        reliabilityFactor {[double]} -- [Reliability Factor]
        Stress Cycle Factor {[double]} -- [Stress Cycle Factor]
    
    Returns:
        [double] -- [Hardness Ratio]
    """
    return allowableStress * stressCycleFactor / reliabilityFactor / bendingStress

def getContactStress(elasticCoefficient, tangentialForce, dynamicFactor, sizeFactor, loadDistributionFactor, pinionDiameter, faceWidth, bendingGeometryFactor):
    """[Calculates Contact Stress]
    
    Arguments:
        elasticCoefficient {[bool]} -- [True if gear is the pinion]
        tangentialForce {[double]} -- [Pinion Hardness]
        dynamicFactor {[double]} -- [Gear Hardness]
        sizeFactor {[double]} -- [Gear Ratio]
        loadDistributionFactor{[double]} -- [Load Distribution Factor]
        pinionDiameter{[double]} -- [Pinion Diameter]
        faceWidth{[double]} -- [Face Width]
        bendingGeometryFactor{[double]} -- [Bending Geometry Factor]
    
    Returns:
        [double] -- [Contact Stress]
    """
    return elasticCoefficient * (tangentialForce * overloadFactor * dynamicFactor * sizeFactor * loadDistributionFactor / (pinionDiameter * faceWidth * bendingGeometryFactor))**0.5

def getContactFactorOfSafety(allowableContactStress, stressCycleFactor, contactStress, hardnessRatioFactor, reliabilityFactor):
    """[Calculates Contact Factor of Safety]
    
    Arguments:
        allowableContactStress {[double]} -- [allowableContactStress]
        stressCycleFactor {[double]} -- [Stress Cycle Factor]
        contactStress {[double]} -- [Contact Stress]
        hardnessRatioFactor {[double]} -- [Hardness Ratio Factor]
        reliabilityFactor{[double]} -- [Reliability Factor]
    
    Returns:
        [double] -- [Contact Factor of Safety]
    """
    return allowableContactStress * stressCycleFactor * hardnessRatioFactor / reliabilityFactor / contactStress

def checkStresses(gearPairDictionary):
    """[Checks if stress levels are allowable]
    Arguments:
        gearPairDictionary {[dictionary]} -- [Dictionary containing all gear information]
    Returns:
        [bool] -- [True if stress is allowable and false if not]
    """
    
    """ Retrieves necessary values from the gear map """
    requiredFactorOfSafety = 2.5 
    tangentialSpeed = gearPairDictionary["tangential_velocity"]
    tangentialForce = gearPairDictionary["tangential_force"]
    pinion = gearPairDictionary["gears"][0]
    gear = gearPairDictionary["gears"][1]
    pMaterial = int(pinion["material"][:4])
    gMaterial = int(gear["material"][:4])
    pinionTeeth = pinion["teeth"]
    gearTeeth = gear["teeth"]
    diametralPitch = pinionTeeth / pinion["pitch_diameter"]
    faceWidth = pinion["face_width"]
    pLewisFormFactor = pinion["Lewis form factor"]
    gLewisFormFactor = gear["Lewis form factor"]
    pBendingGeometryFactor = pinion["geometry factor"]
    gBendingGeometryFactor = gear["geometry factor"]
    
    """ Get material dependent properties """
    pYoungModulus = getElasticModulus(pMaterial)
    pPoisson = getFishRatio(pMaterial)
    pHardness = getBrinellHardness(pMaterial)
    gYoungModulus = getElasticModulus(gMaterial)
    gPoisson = getFishRatio(gMaterial)
    gHardness = getBrinellHardness(gMaterial)
    
    """ Get allowable bending and contact stresses for the gear and pinion """
    pAllowableBendingStress = getAllowableBendingStress(pHardness)
    pAllowableContactStress = getAllowableContactStress(pHardness)
    gAllowableBendingStress = getAllowableBendingStress(gHardness)
    gAllowableContactStress = getAllowableContactStress(gHardness)
    
    """ Calculation of required factors """
    reliabilityFactor = getReliabilityFactor(reliability)
    pDynamicFactor = getDynamicFactor(qualityFactor, tangentialSpeed)
    gDynamicFactor = getDynamicFactor(qualityFactor, tangentialSpeed)
    pSizeFactor = getSizeFactor(diametralPitch, pLewisFormFactor, faceWidth)
    gSizeFactor = getSizeFactor(diametralPitch, gLewisFormFactor, faceWidth)
    loadDistributionFactor = getLoadDistributionFactor(faceWidth, pinionTeeth/diametralPitch, qualityFactor)
    geometryFactorPittingResistance = getGeometryFactorPittingResistance(gearTeeth/pinionTeeth)
    elasticCoefficient = getElasticCoefficient(pPoisson, pYoungModulus, gPoisson, gYoungModulus)
    pHardnessRatioFactor = getHardnessRatioFactor(True, pHardness, gHardness, gearTeeth/pinionTeeth)
    gHardnessRatioFactor = getHardnessRatioFactor(False, pHardness, gHardness, gearTeeth/pinionTeeth)  
    
    """ Calculation of contact and bending stress of pinion and gear """
    pBendingStress = getBendingStress(tangentialForce, pDynamicFactor, pSizeFactor, diametralPitch, faceWidth, loadDistributionFactor, pBendingGeometryFactor)
    gBendingStress = getBendingStress(tangentialForce, gDynamicFactor, gSizeFactor, diametralPitch, faceWidth, loadDistributionFactor, gBendingGeometryFactor)
    pContactStress = getContactStress(elasticCoefficient, tangentialForce, pDynamicFactor, pSizeFactor, loadDistributionFactor, pinionTeeth/diametralPitch, faceWidth, geometryFactorPittingResistance)
    gContactStress = (gSizeFactor / pSizeFactor)**0.5 * pContactStress
    
    """ Calculation of factors of safety """
    pinionBFOS = getBendingFactorOfSafety(pAllowableBendingStress, pBendingStress, reliabilityFactor, bendingStressCycleFactor)
    gearBFOS = getBendingFactorOfSafety(gAllowableBendingStress, gBendingStress, reliabilityFactor, bendingStressCycleFactor)
    pinionCFOS = getContactFactorOfSafety(pAllowableContactStress, pittingStressCycleFactor, pContactStress, pHardnessRatioFactor, reliabilityFactor)
    gearCFOS = getContactFactorOfSafety(gAllowableContactStress, pittingStressCycleFactor, gContactStress, gHardnessRatioFactor, reliabilityFactor)
   
    """ Determine if factor of safety requirement is met """
    if pinionBFOS > requiredFactorOfSafety and gearBFOS > requiredFactorOfSafety and pinionCFOS**2 > requiredFactorOfSafety and gearCFOS**2 > requiredFactorOfSafety:
        return true
    else:
        return false





