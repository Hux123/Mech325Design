import itertools
import json
from conversions import *
from GearBoxObject import *
from MotorInput import *
import matplotlib.pyplot as plt



def readJsonGear(gearsJson):
    """[Reads json files]
    
    Arguments:
        gearsJson {[string]} -- [address of the gears json file]
    
    Returns:
        [list of gear dictionaries] -- [list of the gear dictionaries]
    """
    with open(gearsJson) as json_file:
        gearsList = json.load(json_file)
    return gearsList


def createAllPermutationIndices( overallNumberOfGears, minNumberOfGears = 1, maxNumberOfGears = 10):
    """[Creates all the permutations of the indices to be used with the gearsList]

    Arguments:
        overallNumberOfGears {[int]} -- [total number of available gears]
    
    Keyword Arguments:
        minNumberOfGears {int} -- [min number of gears for the permutation] (default: {1})
        maxNumberOfGears {int} -- [max number of gears for the permutation] (default: {5})
    
    Returns:
        [dictionary of the list of permutations] -- [list of permutations of the indices as a   
                                                    dictionary with the key as the number of 
                                                    elements the permutation]
    """

    keysList = [i for i in range(0,overallNumberOfGears)]
    IndicesPermutationsDictionary = {}
    for numOfGears in range(minNumberOfGears, maxNumberOfGears + 1):
        # We can only have an even number of gears
        if numOfGears % 2 == 0:
            IndicesList =  keysList # * numOfGears
            IndicesPermutationsDictionary[numOfGears] = itertools.permutations(IndicesList, numOfGears)
    
    # print([item for item in IndicesPermutationsDictionary[2]])
    # print([item for item in IndicesPermutationsDictionary[2]])
    return IndicesPermutationsDictionary


def createGearCombinations(numberOfGears, jsonFiles, showFigure = False):
    """[Creates the list of pairs of gear values and carries out the calculation]
    Incomplete for now
    
    Arguments:
        numberOfGears {[int]} -- [desired number of gears]
        jsonFiles {[string]} -- [address of the gears json file]
    
    Keyword Arguments:
        showFigure {bool} -- [I don't know what to return for now ] (default: {False})
    """

    gearsList = readJsonGear(jsonFiles)
    totalNumberOfAvailableGears = len(gearsList)
    permutationIndices = createAllPermutationIndices(totalNumberOfAvailableGears)[numberOfGears]
    omegaList, torqueList = motorValues()

    for indexCombination in permutationIndices:

        thisGearBox = gearBoxObject(gearsList, indexCombination)
        if thisGearBox.validGearBoxPitch():
            print("valid configuration")
            omegaOutputList, torqueOutputList = thisGearBox.createOmegaTorqueGraph(torqueList, omegaList, showPlot = False)

            if showFigure:
                plt.plot(omegaList, torqueList, "blue")
                plt.plot(omegaOutputList, torqueOutputList, "red")
                plt.show()
                plt.clf()
        else:
            print("Invalid configuration ...")
        
        input("Next")
    
    return True









