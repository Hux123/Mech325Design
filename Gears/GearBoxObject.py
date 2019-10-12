from conversions import *

class gearBoxObject():


    def __init__(self, gearsList, indexCombination):
        self.gearSet = []
        for index in indexCombination:
            self.gearSet.append(gearsList[index])
        self.gearPairs = {}
        for pairIndex in range(0,len(indexCombination) - 1):
            self.gearSet[pairIndex]["material"] = self.gearSet[pairIndex]["material"].split(" ")[0]
            self.gearSet[pairIndex]["material"] = self.gearSet[pairIndex + 1]["material"].split(" ")[0] 
            self.gearPairs[pairIndex] = {}
            self.gearPairs[pairIndex]["gears"] = [self.gearSet[pairIndex], self.gearSet[pairIndex + 1]]


    def validGearBoxPitch(self):
        for pairNumber, gearPair in self.gearPairs.items():
            firstGear = gearPair["gears"][0]
            secondGear = gearPair["gears"][1]
            if firstGear["pitch"] != secondGear["pitch"]:
                return False

        return True


    def calc(self, omega, torqueInput):
        omegaSoFar = omega
        torqueSoFar = torqueNmToPoundFeet(torqueInput) * self.gearPairs[0]["gears"][0]["efficiency"] 
        tangentialVelocity = omegaSoFar * (inchToFeet(self.gearPairs[0]["gears"][0]["pitch_diameter"]) / 2)

        for pairIndex, gearPair in self.gearPairs.items():
            firstGear = gearPair["gears"][0]
            secondGear = gearPair["gears"][1]

            gearOmegaRatio = firstGear["teeth"] / secondGear["teeth"] 
            gearTorqueRatio = secondGear["teeth"] / firstGear["teeth"]

            tangentialForce = torqueSoFar / (firstGear["pitch_diameter"] / 2)

            if firstGear["pitch"] != secondGear["pitch"]:
                return False, False, False
            
            self.gearPairs[pairIndex]["tangential_force"] = tangentialForce
            self.gearPairs[pairIndex]["tangential_velocity"] = tangentialVelocity

            torqueSoFar = torqueSoFar * gearTorqueRatio * secondGear["efficiency"]
            omegaSoFar = omegaSoFar * gearOmegaRatio

            print(omegaSoFar)
        input("__________")
        
        finalOmega = omegaSoFar
        finalTorque = torqueSoFar

        return finalOmega, torquePoundFeetToNm(finalTorque), self.gearPairs


    def createOmegaTorqueGraph(self, torqueList, omegaList, showPlot = False):

        omegaOutputList = []
        torqueOutputList = []
        
        for index in range(0, len(torqueList)):
            omega = omegaList[index]
            torque = torqueList[index]
            outputOmega, outputTorque, gearPairs = self.calc(omega, torque)
            # Here we will check the values returned by cailin
            passStressChecks = True
            
            # If we pass, we will add the values
            # Otherwise we will simply add (0,0) to the set
            if passStressChecks:
                omegaOutputList.append(omega)
                torqueOutputList.append(torque)
            else:
                omegaOutputList.append(0)
                torqueOutputList.append(0)
        
        if showPlot:
            plt.plot(omegaOutputList, torqueOutputList)
            plt.show()
            plt.clf()
        
        return omegaOutputList, torqueOutputList
