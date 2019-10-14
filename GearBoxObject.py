from conversions import *
import matplotlib.pyplot as plt
from GearStressCalculations import *


class gearBoxObject():
    """[Gearbox object for any configuration of gears]

    Returns:
        [Gearbox Object] -- [Object representing the properties of any gear configuration]
    """

    def __init__(self, gearsList, indexCombination):
        """[Constructor]
        
        Arguments:
            gearsList {[list of json dictionaries]} -- [list of gears from the json file]
            indexCombination {[list of ints]} -- [indices for this configuration of the gears]
            cost{[double]} -- [price of this gear set]
        """
        self.indexCombination = indexCombination
        self.gearSet = []
        for index in indexCombination:
            gearsList[index]["material"] = gearsList[index]["material"].split(" ")[0]
            self.gearSet.append(gearsList[index])
        self.gearPairs = {}
        self.gearSetPrice = sum(gear["cost"] for gear in self.gearSet)
        pairIndex = 0
        while pairIndex < len(self.gearSet):
            self.gearPairs[pairIndex] = {}
            self.gearPairs[pairIndex]["gears"] = [self.gearSet[pairIndex], self.gearSet[pairIndex + 1]]
            pairIndex += 2


    def validGearBoxPitch(self):
        """[Checks to see if the gearbox is valid, eg: having the same pitches]
        
        Returns:
            [boolean] -- [True or False about whether the gearbox is valid]
        """
        for pairNumber, gearPair in self.gearPairs.items():
            firstGear = gearPair["gears"][0]
            secondGear = gearPair["gears"][1]
            if firstGear["pitch"] != secondGear["pitch"]:
                return False

        return True


    def calc(self, omega, torqueInput):
        """[Does all the calculations for the gear set given an omega and input torque]
        
        Arguments:
            omega {[double]} -- [input rotational rpm]
            torqueInput {[double]} -- [input torque]
        
        Returns:
            [double] -- [the final output omega]
            [double] -- [the final output torque]
            [gear pair] -- [a dictionary of the gear pairs with updated value, eg: tangential velocity and force]
        """

        omegaSoFar = omega
        torqueSoFar = torqueNmToPoundFeet(torqueInput) * self.gearPairs[0]["gears"][0]["efficiency"] 

        # Dictionary sent to Cailing for stress analysis
        stressAnalysisPairs = {}

        for pairIndex, gearPair in self.gearPairs.items():
            firstGear = gearPair["gears"][0]
            secondGear = gearPair["gears"][1]

            gearOmegaRatio = firstGear["teeth"] / secondGear["teeth"] 
            gearTorqueRatio = secondGear["teeth"] / firstGear["teeth"]

            tangentialForce = torqueSoFar / (firstGear["pitch_diameter"] / 2)
            tangentialVelocity = omegaSoFar * (firstGear["pitch_diameter"] / 2)

            self.gearPairs[pairIndex]["tangential_force"] = tangentialForce
            self.gearPairs[pairIndex]["tangential_velocity"] = tangentialVelocity

            torqueSoFar = torqueSoFar * gearTorqueRatio * secondGear["efficiency"]
            omegaSoFar = omegaSoFar * gearOmegaRatio

            # This is what Cailin required
            # Smaller gear first
            stressAnalysisPairs[pairIndex] = {}
            if firstGear["teeth"] > secondGear["teeth"]:
                stressAnalysisPairs[pairIndex]["gears"] = [secondGear, firstGear]
            else:
                stressAnalysisPairs[pairIndex]["gears"] = [firstGear, secondGear]
            
            stressAnalysisPairs[pairIndex]["tangential_force"] = tangentialForce
            stressAnalysisPairs[pairIndex]["tangential_velocity"] = tangentialVelocity

        
        finalOmega = omegaSoFar
        finalTorque = torqueSoFar

        return finalOmega, torquePoundFeetToNm(finalTorque), self.gearPairs

    def createOmegaTorqueGraph(self, torqueList, omegaList, showPlot = False):
        """[Creates the omegavs torque graph for the input motor values for this configuration of gears]
        
        Arguments:
            torqueList {[list of double]} -- [list of the possible input torque values of the motor]
            omegaList {[list of double]} -- [list of the possible input rpm values of the motor]
        
        Keyword Arguments:
            showPlot {bool} -- [requires to be truw in order to show the plot] (default: {False})
        
        Returns:
            [list of double] -- [list of omega outputs]
            [list of double] -- [list of torque outputs]
        """

        omegaOutputList = []
        torqueOutputList = []
        
        for index in range(0, len(torqueList)):
            omega = omegaList[index]
            torque = torqueList[index]
            outputOmega, outputTorque, stressAnalysisPairs = self.calc(omega, torque)
            
            # Here we will check the values returned by Cailin
            # We will consider this function for all the gear sets
            passStressChecks = True
            for gearPairKey in stressAnalysisPairs.keys():
                gearPairDictionary = stressAnalysisPairs[gearPairKey]
                thisGearPairStressChecks = checkStresses(gearPairDictionary)
                if thisGearPairStressChecks == False:
                    passStressChecks = False
                    break

            # If we pass, we will add the values
            # Otherwise we will simply add (0,0) to the set
            if passStressChecks:
                omegaOutputList.append(outputOmega)
                torqueOutputList.append(outputTorque)
            else:
                omegaOutputList.append(0)
                torqueOutputList.append(0)
        
        if showPlot:
            plt.plot(omegaOutputList, torqueOutputList)
            plt.show()
            plt.clf()
        
        return omegaOutputList, torqueOutputList
