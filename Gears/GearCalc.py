import itertools
import json
from conversions import *
from GearBoxObject import *
from MotorInput import *



def readJsonGear(gearsJson):
    with open(gearsJson) as json_file:
        gearsList = json.load(json_file)
    return gearsList

def createAllPermutationIndices(minNumberOfGears = 1, maxNumberOfGears = 5):
    keysList = [i for i in range(minNumberOfGears,maxNumberOfGears)]
    IndicesPermutationsDictionary = {}
    for numOfGears in range(minNumberOfGears, maxNumberOfGears + 1):
        IndicesList =  keysList * numOfGears
        IndicesPermutationsDictionary[numOfGears] = itertools.permutations(IndicesList, numOfGears)
    return IndicesPermutationsDictionary


def createPairsList(numberOfGears, jsonFiles, showFigure = False):
    permutationIndices = createAllPermutationIndices()[numberOfGears]
    gearsList = readJsonGear(jsonFiles)
    omegaList, torqueList = motorValues()

    for indexCombination in permutationIndices:

        thisGearBox = gearBoxObject(gearsList, indexCombination)
        if thisGearBox.validGearBoxPitch():
            print("valid configuration")
            omegaOutputList, torqueOutputList = thisGearBox.createOmegaTorqueGraph(torqueList, omegaList, showPlot = False)
            
            if showFigure:
                plt.plot(omegaList, torqueList, "blue")
                # plt.plot(omegaOutputList, torqueOutputList, "red")
                plt.show()
                plt.clf()
        else:
            print("Invalid configuration ...")
        
        input("Next")
    
    return









