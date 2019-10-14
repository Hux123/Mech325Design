
# coding: utf-8

# In[13]:


import numpy as np
import math
import math
from matplotlib import pyplot as plt


# In[25]:


class powerScrewObject():
    """[This is he power screw object]

    Returns:
        [type] -- [description]
    """
    def __init__(self):
        self.powerScrewPitch = 0.00508 #m/rotation
        self.powerScrewMajorDiameter = 0.01905 #m
        self.frictionCoeff = 0.2
        self.threadAngle = 29  #degrees
        self.pistonDiameter = 0.1 #m
        self.powerScrewCost = 9.38   

    def asDict(self):
        """[returns object as a dictionary]
        
        Returns:
            [dictionary] -- [object as a dictionary]
        """
        powerScrewDict = {"powerScrewCost": self.powerScrewCost,
                          "powerScrewmajorDiameter": self.powerScrewMajorDiameter,
                          "frictionCoeff": self.frictionCoeff,
                          "threadAngle": self.threadAngle,
                          "pistonDiameter": self.pistonDiameter,
                          "powerScrewCost": self.powerScrewCost}
        return powerScrewDict

    

#Define constants of power screw
powerScrewPitch = 0.00508 #m/rotation
powerScrewMajorDiameter = 0.01905 #m
frictionCoeff = 0.2
threadAngle = 29  #degrees
pistonDiameter = 0.1 #m
powerScrewCost = 9.38

pistonArea = math.pi*(pistonDiameter)**2 #mm^2

#Define useful functions
def calculatePerformance(rpm,cost):
    return (calculateOutputFlow(rpm)/cost)

#Returns mL/s
def calculateOutputFlow(rpm):
    pistonVelocity = findPistonVelocity(rpm,powerScrewPitch)
    return pistonVelocity * pistonArea * 10**(6)
    
def calculateMeanDiameter(majorDiameter, pitch):
    return majorDiameter - pitch/2

def secant(angle):
    return 1/math.cos(angle)

#Returns m/s units
def findPistonVelocity(rpm,powerScrewPitch):
    rotationsPerSec = rpm/60.0
    return rotationsPerSec*powerScrewPitch

#Returns pressure in Pa units
def findPressure(pistonVelocity):
    return (5*10**6)*pistonVelocity

#Returns force in N units
def findForce(pistonPressure):
    return pistonPressure*pistonArea

#F: force applied to piston
#l: pitch of power screw
#dm: major diameter
#f: friction coefficient
#alpha: pitch angle
def powerScrewTorque(F,l,dm,f,alpha):
    Torque = ((F*dm)/2)*((l+math.pi*f*dm*secant(alpha*(math.pi/180)))/(math.pi*dm-f*l*secant(alpha*(math.pi/180))))
    return Torque


