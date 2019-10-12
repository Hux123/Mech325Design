from conversions import *
import matplotlib.pyplot as plt

def motorValues(showPlot = False):
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


