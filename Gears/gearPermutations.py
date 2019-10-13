import json
import itertools


def createAllPermutations(gearsJson, minNumberOfGears = 1, maxNumberOfGears = 5):
    
    with open(gearsJson) as json_file:
        gearsList = json.load(json_file)

    permutationDictionary = {}
    gearKeys = list(gearsList.keys())
    for numOfGears in range(minNumberOfGears, maxNumberOfGears + 1):
        thisGroupList = gearKeys * numOfGears
        thisNumberOfGearsPermutations = itertools.permutations(thisGroupList, numOfGears)
        for i in thisNumberOfGearsPermutations:
            print(i)
        input()
    return


gearJson = 'gearsJson.json'
createAllPermutations(gearJson)