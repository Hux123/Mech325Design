import itertools
import json
# import tqdm
from conversions import *
from GearBoxObject import *
from MotorInput import *
from GearCalc import *
import matplotlib.pyplot as plt
from PowerScrewOutput import *
from Intersection import *


def ShowResults(numberOfGears, jsonFiles, showFigure = False):
    """[Creates the list of pairs of gear values and carries out the calculation]
    Incomplete for now
    
    Arguments:
        numberOfGears {[int]} -- [desired number of gears]
        jsonFiles {[string]} -- [address of the gears json file]
    
    Keyword Arguments:
        showFigure {bool} -- [I don't know what to return for now ] (default: {False})
    """

    #First we Calculate the power screw info
    powerScrewMeanDiameter = calculateMeanDiameter(powerScrewMajorDiameter,powerScrewPitch)

    #Create array of possible RPM's to graph
    rpmList = np.arange(0,2000,1)
    pistonVelocity = findPistonVelocity(rpmList ,powerScrewPitch)
    chamberPressure = findPressure(pistonVelocity)
    requiredForce = findForce(chamberPressure)
    powerScrewTorqueList = powerScrewTorque(requiredForce,powerScrewPitch,powerScrewMeanDiameter,frictionCoeff,threadAngle/2)


    gearsList = readJsonGear(jsonFiles)
    totalNumberOfAvailableGears = len(gearsList)
    permutationIndices = createAllPermutationIndices(totalNumberOfAvailableGears)[numberOfGears]
    motorOmegaList, motorTorqueList = motorValues()

    for indexCombination in permutationIndices:
        print(permutationIndices)
        print("_____________________________")
        thisGearBox = gearBoxObject(gearsList, indexCombination)
        if thisGearBox.validGearBoxPitch():
            print("valid configuration")
            gearBoxOmegaOutputList, gearBoxTorqueOutputList= thisGearBox.createOmegaTorqueGraph(motorTorqueList, motorOmegaList, showPlot = False)
            if showFigure:
                plt.plot(motorOmegaList, motorTorqueList, "blue", label = "Motor")
                plt.plot(gearBoxOmegaOutputList, gearBoxTorqueOutputList, "red", label = "GearBox")
                plt.plot(rpmList, powerScrewTorqueList, "green", label = "PowerScrew")
                plt.show()
                plt.clf()
        else:
            print("Invalid configuration ...")
        
        input("Next")
    
    return True


def FindBest(numberOfGears, jsonFiles, showFigure = True):
    """[Creates the list of pairs of gear values and carries out the calculation
    Finds the best value ratio for rpm/price]
    Incomplete for now
    
    Arguments:
        numberOfGears {[int]} -- [desired number of gears]
        jsonFiles {[string]} -- [address of the gears json file]
    
    Keyword Arguments:
        showFigure {bool} -- [I don't know what to return for now ] (default: {False})
    """

    #First we Calculate the power screw info
    powerScrewMeanDiameter = calculateMeanDiameter(powerScrewMajorDiameter,powerScrewPitch)

    #Create array of possible RPM's to graph
    rpmList = np.arange(0,5000,1)
    pistonVelocity = findPistonVelocity(rpmList ,powerScrewPitch)
    chamberPressure = findPressure(pistonVelocity)
    requiredForce = findForce(chamberPressure)
    powerScrewTorqueList = powerScrewTorque(requiredForce,powerScrewPitch,powerScrewMeanDiameter,frictionCoeff,threadAngle/2)
    powerScrew = powerScrewObject()


    bestOutPutScore = 0
    bestTorque = 0
    bestOmega = 0
    bestGearBoxOmegaOutputList = []
    bestGearBoxTorqueOutputList = []
    bestPowerScrewTorqueList = []
    bestPowerScrewRPMList = []
    bestGearSet = None
    bestMotorInput = [0,0]
    bestOutputFlowRate= 0


    gearsList = readJsonGear(jsonFiles)
    totalNumberOfAvailableGears = len(gearsList)
    permutationIndices = createAllPermutationIndices(totalNumberOfAvailableGears)[numberOfGears]
    motorOmegaList, motorTorqueList = motorValues()

    print("working")


    # for indexCombination in permutationIndices:
    for indexCombination in permutationIndices:
        print(indexCombination)

        thisGearBox = gearBoxObject(gearsList, indexCombination)
        if thisGearBox.validGearBoxPitch():
            # print("valid configuration")
            gearBoxOmegaOutputList, gearBoxTorqueOutputList= thisGearBox.createOmegaTorqueGraph(motorTorqueList, motorOmegaList, showPlot = False)
            

            intersectionRPM, intersectionTorque, motorOmegaInput, motorTorqueInput  = findIntersection([gearBoxOmegaOutputList, gearBoxTorqueOutputList],[rpmList,powerScrewTorqueList], [motorOmegaList, motorTorqueList])
            
            thisOutputFlowRate = calculateOutputFlow(intersectionRPM)
            # thisOutputScore = thisOutputFlowRate / float(thisGearBox.gearSetPrice + powerScrewCost)
            thisOutputScore = intersectionRPM

            print(intersectionRPM)

            motorInput = [motorOmegaInput, motorTorqueInput]


            if thisOutputScore > bestOutPutScore:
                # print("updating")
                bestOutPutScore = thisOutputScore
                bestTorque = intersectionTorque
                bestOmega = intersectionRPM
                bestGearBoxOmegaOutputList = gearBoxOmegaOutputList
                bestGearBoxTorqueOutputList = gearBoxTorqueOutputList
                bestPowerScrewTorqueList = rpmList
                bestPowerScrewRPMList = powerScrewTorqueList
                bestGearSet = thisGearBox
                bestMotorInput = motorInput
                bestOutputFlowRate = thisOutputFlowRate
        else:
            pass
            # print("Invalid configuration ...")
    
    # print(bestGearSet.asDict())

    solution = {
                "motor_input" : bestMotorInput,
                "gear_set": bestGearSet.asDict(),
                "gearbox_omega_list" : bestGearBoxOmegaOutputList,
                "gearbox_torque_lsit" : bestGearBoxTorqueOutputList,
                "power_screw": powerScrew.asDict(),
                "power_screw_omega_list" : bestPowerScrewRPMList.tolist(),
                "power_screw_torque_list" : bestPowerScrewTorqueList.tolist(),
                "intersection_rpm": bestOmega,
                "intersection_torque": bestTorque,
                "score": bestOutPutScore,
                "flowrate": bestOutputFlowRate
                 }
    
    # Saving the solution
    with open('Solution.json', 'w') as fp:
        json.dump(solution, fp)

    if showFigure:
            print("The best output was: ", bestOutPutScore)
            print("Best torque: ", bestTorque)
            print("Best RPM: ", bestOmega)
            print("best flowrate: ", bestOutputFlowRate)
            plt.plot(motorOmegaList, motorTorqueList, "blue", label = "Motor")
            plt.plot(bestGearBoxOmegaOutputList, bestGearBoxTorqueOutputList, "red", label = "GearBox")
            plt.plot(bestPowerScrewRPMList, powerScrewTorqueList, "green", label = "PowerScrew")
            plt.xlabel("RPM")
            plt.ylabel("Best case graph")
            plt.title("Torque vs RPM")
            plt.show()
            plt.clf()
    
    return True

print("running")
FindBest(2, "gear_data.json", True)
# """[run function required]
# """


# ShowResults(2, "gear_data.json", True)
