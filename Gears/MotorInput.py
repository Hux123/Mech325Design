from conversions import *
import matplotlib.pyplot as plt

def motorValues(showPlot = False):
    """[Motor value equation function]
    
    Keyword Arguments:
        showPlot {bool} -- [choose true to see the plot] (default: {False})
    
    Returns:
        [list of doubles] -- [list of output rpm of the motor]
        [list of doubles] -- [list of output torques of the motor]
    """
    omegaList = []
    torqueList = []
    for omega in range(0,5000,1):
        omegaList.append(omega)
        torque = 5 - omega / 1000
        torqueList.append(torque)
    
    if showPlot:
        plt.plot(omegaList, torqueList)
        plt.show()
        plt.clf()
    
    return omegaList, torqueList


