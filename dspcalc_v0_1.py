import math
import blessed
import json
import os

#global variables
timeUnitModifier = {"second":1, "minute":60, "hour":3600} #index using "timeUnit"
proliferatorBonus = {"none":1, "mki":1.125, "mkii":1.2, "mkiii":1.25}
machineList = []
machineMaxLevel = {"assembling machine": 4, "chemical plant": 2, "smelter": 3, "particle collider": 1, "oil refinery": 1, "matrix lab": 2, "proliferator": 3}
machineSpeedDictionary = {"assembling machine": {1: 0.75, 2: 1, 3: 1.5, 4:3}, "chemical plant": {1: 1, 2: 2}, "smelter": {1: 1, 2: 2}, "particle collider": {1: 1}, "oil refinery": {1: 1}, "matrix lab": {1:1, 2:3}}
possibleRareMatsOptionsList = [] #this is stupid but it works and I don't want to figure something else out right now
configFilepath = os.path.abspath(r"config\config.json")

#changeable globals
try:
    with open(configFilepath, 'r') as file:
        timeUnit, proliferatorLevel, machineLevelUsed, usableRareMats = json.load(file)
except FileNotFoundError:
    timeUnit = "minute"
    proliferatorLevel = "mkiii"
    machineLevelUsed = {"assembling machine": 3, "chemical plant": 2, "smelter": 2, "particle collider": 1, "oil refinery": 1, "matrix lab": 1, "proliferator": 3}
    usableRareMats = {"kimberlite ore": 'N', "fractal silicon": 'N', "optical grating crystal": 'N', "spiniform stalagmite crystal": 'N', "unipolar magnet": 'N', "fire ice": 'N', 'organic crystal': 'N'}
    
    saveList = [timeUnit, proliferatorLevel, machineLevelUsed, usableRareMats]
    
    with open(configFilepath, 'w') as file:
        json.dump(saveList, file)
except:
    print("Something has gone HORRIBLY wrong with the settings. \nDM u/FactoryBuilder. He'll be impressed if this code actually executes")

#List of raw materials. Necessary for formatting().
rawMaterialList = ["iron ore", "copper ore", "stone", "coal", "silicon ore", "titanium ore", "kimberlite ore", "fractal silicon", "optical grating crystal", "spiniform stalagmite crystal", "unipolar magnet", "fire ice", "organic crystal", "critical photon", "crude oil", "hydrogen", "water"]


#RELIC! RECIPES NOW EXIST IN AN EXTERNAL .JSON FILE. THIS IS NOT USED. (the variable name is though but it's not defined here)
"""recipeDictionary = {# FORMAT: "magnetic coil: {"machine": "assembling machine", "producedAmount": 2, "timeToMake": 1, "magnet": 2, "copper ingot": 1}
                    "iron ore": {"machine": None, "producedAmount": 1, "timeToMake": 1},
                    "copper ore": {"machine": None, "producedAmount": 1, "timeToMake": 1},
                    "stone": {"machine": None, "producedAmount": 1, "timeToMake": 1},
                    "coal": {"machine": None, "producedAmount": 1, "timeToMake": 1},
                    "silicon ore": {"machine": None, "producedAmount": 1, "timeToMake": 1},
                    "titanium ore": {"machine": None, "producedAmount": 1, "timeToMake": 1},
                    "kimberlite ore": {"machine": None, "producedAmount": 1, "timeToMake": 1},
                    "fractal silicon": {"machine": None, "producedAmount": 1, "timeToMake": 1},
                    "optical grating crystal": {"machine": None, "producedAmount": 1, "timeToMake": 1},
                    "spiniform stalagmite crystal": {"machine": None, "producedAmount": 1, "timeToMake": 1},
                    "unipolar magnet": {"machine": None, "producedAmount": 1, "timeToMake": 1},
                    "fire ice": {"machine": None, "producedAmount": 1, "timeToMake": 1},
                    "critical photon": {"machine": None, "producedAmount": 1, "timeToMake": 1},
                    "crude oil": {"machine": None, "producedAmount": 1, "timeToMake": 1},
                    "hydrogen": {"machine": None, "producedAmount": 1, "timeToMake": 1},
                    "refined oil": {"machine": "oil refinery", "producedAmount": 3, "timeToMake": 4, "refined oil": 2, "hydrogen": 1, "coal": 1},
                    "water": {"machine": None, "producedAmount": 1, "timeToMake": 1},
                    "iron ingot": {"machine": "smelter", "producedAmount": 1, "timeToMake": 1, "iron ore": 1},
                    "copper ingot": {"machine": "smelter", "producedAmount": 1, "timeToMake": 1, "copper ore": 1},
                    "stone brick": {"machine": "smelter", "producedAmount": 1, "timeToMake": 1, "stone": 1},
                    "energetic graphite": {"machine": "smelter", "producedAmount": 1, "timeToMake": 2, "coal": 2},
                    "high purity silicon": {"machine": "smelter", "producedAmount": 1, "timeToMake": 2, "silicon ore": 2},
                    "titanium ingot": {"machine": "smelter", "producedAmount": 1, "timeToMake": 2, "titanium ore": 2},
                    "magnet": {"machine": "smelter", "producedAmount": 1, "timeToMake": 1.5, "iron ore": 1},
                    "magnetic coil": {"machine": "assembling machine", "producedAmount": 2,  "timeToMake": 1, "magnet": 2, "copper ingot": 1},
                    "glass": {"machine": "smelter", "producedAmount": 1, "timeToMake": 2, "stone": 2},
                    "diamond": {"normal": {"machine": "smelter", "producedAmount": 1, "timeToMake": 2, "energetic graphite": 1}, "kimberlite ore": {"machine": "smelter", "producedAmount": 2, "timeToMake": 1.5, "kimberlite ore": 1}},
                    "crystal silicon": {"normal": {"machine": "smelter", "producedAmount": 1, "timeToMake": 2, "high purity silicon": 1}, "fractal silicon": {"machine": "assembling machine", "producedAmount": 2, "timeToMake": 1.5, "fractal silicon": 1}},
                    "titanium alloy": {"machine": "smelter", "producedAmount": 4, "timeToMake": 12, "titanium ingot": 4, "steel": 4, "sulfuric acid": 8},
                    "steel": {"machine": "smelter", "producedAmount": 1, "timeToMake": 3, "iron ingot": 3},
                    "circuit board": {"machine": "assembling machine", "producedAmount": 2, "timeToMake": 1, "iron ingot": 2, "copper ingot": 1},
                    "prism": {"machine": "assembling machine", "producedAmount": 2, "timeToMake": 2, "glass": 3},
                    "electric motor": {"machine": "assembling machine", "producedAmount": 1,  "timeToMake": 2, "iron ingot": 2, "gear": 1, "magnetic coil": 1},
                    "microcrystalline component": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 2, "high purity silicon": 2, "copper ingot": 1},
                    "proliferator mki": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 0.5, "coal": 1},
                    "gear": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 1, "iron ingot": 1},
                    "plasma exciter": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 2, "magnetic coil": 4, "prism": 2},
                    "photon combiner": {"normal": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 3, "prism": 2, "circuit board": 1}, "optical grating crystal": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 3, "optical grating crystal": 1, "circuit board": 1}},
                    "electromagnetic turbine": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 2, "electric motor": 2, "magnetic coil": 2},
                    "processor": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 3, "circuit board": 2, "microcrystalline component": 2},
                    "proliferator mkii": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 1, "proliferator mki": 2, "diamond": 1},
                    "foundation": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 1, "stone brick": 3, "steel": 1},
                    "particle container": {"normal": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 4, "electromagnetic turbine": 2, "copper ingot": 2, "graphene": 2}, "unipolar magnet": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 4, "unipolar magnet": 10, "copper ingot": 2}},
                    "super magnetic ring": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 3, "electromagnetic turbine": 2, "magnet": 3, "energetic graphite": 1},
                    "graviton lens": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 6, "diamond": 4, "strange matter": 1},
                    "proliferator mkiii": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 2, "proliferator mkii": 2, "carbon nanotubes": 1},
                    "deuterium": {"machine": "particle collider", "producedAmount": 5, "timeToMake": 2.5, "hydrogen": 10},
                    "sulfuric acid": {"machine": "chemical plant", "producedAmount": 4, "timeToMake": 6, "refined oil": 6, "stone": 8, "water": 4},
                    "hydrogen fuel rod": {"machine": "assembling machine", "producedAmount": 2, "timeToMake": 6, "titanium ingot": 1, "hydrogen": 10},
                    "deuteron fuel rod": {"machine": "assembling machine", "producedAmount": 2, "timeToMake": 12, "titanium alloy": 1, "deuterium": 20, "super magnetic ring": 1},
                    "antimatter fuel rod": {"machine": "assembling machine", "producedAmount": 2, "timeToMake": 24, "antimatter": 12, "hydrogen": 12, "annihilation constraint sphere": 1, "titanium alloy": 1},
                    "plastic": {"machine": "chemical plant", "producedAmount": 1, "timeToMake": 3, "refined oil": 2, "energetic graphite": 1},
                    "organic crystal": {"normal": {"machine": "chemical plant", "producedAmount": 1, "timeToMake": 6, "plastic": 2, "refined oil": 1, "water": 1}, "organic crystal": {"machine": None, "producedAmount": 1, "timeToMake": 1}},
                    "graphene": {"normal": {"machine": "chemical plant", "producedAmount": 2, "timeToMake": 3, "energetic graphite": 3, "sulfuric acid": 1}, "fire ice": {"machine": "chemical plant", "producedAmount": 2, "timeToMake": 2, "fire ice": 2, "byproduct": {"hydrogen":1}}},
                    "annihilation constraint sphere": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 20, "particle container": 1, "processor": 1},
                    "casimir crystal": {"normal": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 4, "titanium crystal": 1, "graphene": 2, "hydrogen": 12}, "optical grating crystal": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 4, "optical grating crystal": 8, "graphene": 2, "hydrogen": 12}},
                    "strange matter": {"machine": "particle collider", "producedAmount": 1, "timeToMake": 8, "particle container": 2, "iron ingot": 2, "deuterium": 10},
                    "titanium crystal": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 4, "organic crystal": 1, "titanium ingot": 3},
                    "carbon nanotubes": {"normal": {"machine": "chemical plant", "producedAmount": 2, "timeToMake": 4, "graphene": 3, "titanium ingot": 1}, "spiniform stalagmite crystal": {"machine": "chemical plant", "producedAmount": 2, "timeToMake": 4, "spiniform stalagmite crystal": 6}},
                    "particle broadband": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 8, "carbon nanotubes": 2, "crystal silicon": 2, "plastic": 1},
                    "thruster": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 4, "steel": 2, "copper ingot": 3},
                    "reinforced thruster": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 6, "titanium alloy": 5, "electromagnetic turbine": 5},
                    "logistics bot": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 2, "iron ingot": 2, "electromagnetic turbine": 1, "processor": 1},
                    "logistics drone": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 4, "iron ingot": 5, "processor": 2, "thruster": 2},
                    "logistics vessel": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 6, "titanium ingot": 10, "processor": 10 , "reinforced thruster": 2},
                    "space warper": {"machine": "assembling machine", "producedAmount": 8, "timeToMake": 10, "gravity matrix": 1},
                    "titanium glass": {"machine": "assembling machine", "producedAmount": 2, "timeToMake": 5, "glass": 2, "titanium ingot": 2, "water": 2},
                    "plane filter": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 12, "casimir crystal": 1, "titanium glass": 2},
                    "antimatter": {"machine": "particle collider", "producedAmount": 2, "timeToMake": 2, "critical photon": 2, "byproduct": {"hydrogen": 2}},
                    "quantum chip": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 6, "processor": 2, "plane filter": 2},
                    "solar sail": {"machine": "assembling machine", "producedAmount": 2, "timeToMake": 4, "graphene": 1, "photon combiner": 1},
                    "frame material": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 6, "carbon nanotubes": 4, "titanium alloy": 1, "high purity silicon": 1},
                    "dyson sphere component": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 8, "frame material": 3, "solar sail": 3, "processor": 3},
                    "small carrier rocket": {"machine": "assembling machine", "producedAmount": 1, "timeToMake": 6, "dyson sphere component": 2, "deuteron fuel rod": 4, "quantum chip": 2},
                    "electromagnetic matrix": {"machine": "matrix lab", "producedAmount": 1, "timeToMake": 3, "magnetic coil": 1, "circuit board": 1},
                    "energy matrix": {"machine": "matrix lab", "producedAmount": 1, "timeToMake": 6, "energetic graphite": 2, "hydrogen": 2},
                    "structure matrix": {"machine": "matrix lab", "producedAmount": 1, "timeToMake": 8, "diamond": 1, "titanium crystal": 1},
                    "information matrix": {"machine": "matrix lab", "producedAmount": 1, "timeToMake": 10, "processor": 2, "particle broadband": 1},
                    "gravity matrix": {"machine": "matrix lab", "producedAmount": 2, "timeToMake": 24, "graviton lens": 1, "quantum chip": 1},
                    "universe matrix": {"machine": "matrix lab", "producedAmount": 1, "timeToMake": 15, "electromagnetic matrix": 1, "energy matrix": 1, "structure matrix": 1, "information matrix": 1, "gravity matrix": 1, "antimatter": 1}
                }"""

recipeDictFilepath = os.path.abspath(r"config\recipes.json")

with open(recipeDictFilepath, "r") as recipeFile:
    recipeDictionary = json.load(recipeFile)

endToStartResults = [] #list containing dictionaries that contain the results of calculations. Needs to be global to survive the recursion

def findItemRecipe(itemDictionary):
    itemRecipe = recipeDictionary[itemDictionary["name"]] #itemRecipe is a dictionary containing:
                                                          #"machine" : string name of the machine used to produce
                                                          #"producedAmount : usually 1 but some recipes produce more than 1 product.
                                                          #"timeToMake" : associated time in seconds, 
                                                          #For each ingredient, "<ingredient name>" : amount for 1 completed recipe
    
    if "normal" in list(itemRecipe.keys()):
        rareMatName = list(itemRecipe.keys())[1] #The [1] index of "itemRecipe.keys()" is the name of the rareMat
        if usableRareMats[rareMatName] == 'Y':
            itemRecipe = itemRecipe[rareMatName] #if rareMat available, use rareMat recipe
        else:
            itemRecipe = itemRecipe["normal"] #if no rareMat available, use normal recipe
    
    return itemRecipe

def byproduct(returnList):
    endToStartResultsBPversion, producedByproductAmount = returnList
    
    if producedByproductAmount:
        found = False
        iterable = iter(endToStartResultsBPversion)
        while not found:
            iteration = next(iterable, None)
            if iteration == None:
                found = True
                endToStartResultsBPversion.append({"name": "byproduct", "producedAmount": producedByproductAmount})
            elif iteration["name"] == "hydrogen":
                iteration["producedAmount"] -= producedByproductAmount
                if iteration["producedAmount"] < 0:
                    found = True
                    endToStartResultsBPversion.append({"name": "byproduct", "baseProductionRate": (iteration[producedAmount] * -1)}) #make a byproducts dictionary with the amount of hydrogen produced (which is negative) turned into a positive as the "baseProductionRate" value. 
                    endToStartResultsBPversion.pop(endToStartResultsBPversion.index(iteration)) #remove hydrogen dictionary
            
    return endToStartResultsBPversion

def endToStart(itemDictionary, recursiveIngredient=False): #Contains the name of the item and the amount needed to be produced per second.
    global endToStartResults
    
    itemRecipe = findItemRecipe(itemDictionary)
    
    unproliferatedProductionRate = itemDictionary["amountPerSecond"] / proliferatorBonus[proliferatorLevel]
    #How much we would produce without proliferator bonus. Because *with* the bonus, it brings us to the needed rate.
    
    ingredientsToCalculate = []
    for ingredient, amount in itemRecipe.items(): #amount is per batch
        if ingredient in recipeDictionary:
            ratio = amount / itemRecipe["producedAmount"]
            neededIngredientRate = ratio * unproliferatedProductionRate
            ingredientDictionary = {"name":ingredient,"amountPerSecond":neededIngredientRate}
            ingredientsToCalculate.append(ingredientDictionary)
    
    results = {"name":itemDictionary["name"],"baseProductionRate":unproliferatedProductionRate}
    
    for dictionary in ingredientsToCalculate:
        results[dictionary["name"]] = dictionary["amountPerSecond"]
    #finished results should look like this for producing 30 magnetic coil/s w/ MKIII proliferator
    #{"name":"magnetic coil","baseProductionRate":24,"magnet":24,"copper ingot":12}
    
    producedByproductAmount = 0
    #Adding byproducts if required
    if "byproduct" in itemRecipe:
        factor = itemDictionary["amountPerSecond"]/ itemRecipe["producedAmount"]
        producedByproductAmount += itemRecipe["byproduct"]["hydrogen"] * factor #hardcoded for hydrogen, fix later if needed.
        
    matched = False #variable to check if we found a match in endToStartResults
    for dictionary in endToStartResults: #endToStartResults is a list of dictionaries that all look like the above example
        if results["name"] == dictionary["name"]: #check to see if the item we just calculated already exists in the endToStartResults dictionaries. If it does, add the results to the existing dictionary.
            matched = True
            for item in dictionary: #for every ingame item, add the number from "results" to "dictionary"
                if item != "name": #ignore the name of the end product
                    dictionary[item] += results[item]
    if matched == False: #No match? Append.
        endToStartResults.append(results)
        
    for ingredient_dictionary in ingredientsToCalculate: #Note: ingredient_dictionary is different from ingredientDictionary
        if ingredient_dictionary["name"] == itemDictionary["name"]:  #IIRC, this is supposed to stop an infinite recursion from the refined oil recipe.
            continue
        endToStart(ingredient_dictionary) #This will do everything above for each ingredient and their ingredients and their ingredients, etc, etc.
    
    return [endToStartResults, producedByproductAmount]

def numMachineCalc(overallResults): #We do this after doing the calculations for how many items we need because we could need the same item at different points in the recipe and the cumulative amount of needed items might require an assembler or two less than the individual amounts would require.
    #overallResults is expected to be the value returned by "endToStart" (which was modified by byproduct(). Variable has the same format.)
    for result in overallResults:
        if result["name"] != "byproduct": #skip byproduct dict
            itemRecipe = findItemRecipe(result) #gets the recipe for the item
            usingMachine = itemRecipe["machine"] #asks which machine we are using
            if result["name"] == "refined oil": #gonna just squeeze this in. If it's the refined oil results, do this and then skip everything else. Refined oil is funky with its recipe. The numOfMachines is simply 4x the needed base rate. I did a bunch of math on paper that determined this.
                numOfMachines = math.ceil(result["baseProductionRate"] * (4 / machineSpeedDictionary[usingMachine][machineLevelUsed[usingMachine]])) #if Youthcat ever comes out with a faster oil refinery, this code will still work. It's 4x refineries if the speed is 1.
                result["numOfMachines"] = numOfMachines
                continue
            if itemRecipe["machine"]:
                numOfMachines = math.ceil(result["baseProductionRate"] / (itemRecipe["producedAmount"]/(itemRecipe["timeToMake"]/machineSpeedDictionary[usingMachine][machineLevelUsed[usingMachine]])))
                # Break down the above math:
                #Number of products produced every second, divided by (time to complete one recipe, divided by the production speed modifier)
                # and use ceil() to round up because you can't have half an assembler
            
                # machineSpeedDictionary[usingMachine][machineLevelUsed[usingMachine]]
                #   asks machineLevelUsed which level we are using of the machine needed in this calculation (specified by the user before calculations)
                #   Then asks machineSpeedDictionary what the production speed modifier of that machine is.
                # machineSpeedDictionary is a dictionary with every machine type as keys and a dictionary as their values. The dictionary contains all possible levels of that machine as keys and speed modifiers as values
        
                result["numOfMachines"] = numOfMachines #append to the result dictionary. #which comes from the overallResults dictionary
        
    return overallResults
        
def formatting(overallResults): #Takes the overallResults and puts them into an easy to read format for humans. Puts it in a text document.
        #overallResults is a list of dictionaries, each of which follows the below example:
        #{"name":"magnetic coil","baseProductionRate":24,"magnet":24,"copper ingot":12,"numOfMachines":12}
        #name of the product, the amount produced every second w/o proliferator bonus, and then each ingredient with their needed rates, followed lastly by the number of machines needed
        
        finishedResults = ""
        totalNumMachines = {"assembling machine": 0, "chemical plant": 0, "smelter": 0, "particle collider": 0, "oil refinery": 0, "matrix lab": 0}
        separator = "\n=================================================\n" #inserts itself between two lines, you do not need to add \n to the end of your entry
        
        for dictionary in overallResults.copy(): #Products # Need to copy overallResults so that we reference the correct indices in overallResults. If we didn't, we'd be popping the wrong dictionaries as we go down the list.
            if ((dictionary["name"] not in rawMaterialList) and (dictionary["name"] != "byproduct")) or ((dictionary["name"] == "organic crystal") and (usableRareMats["organic crystal"] == "N")): # If the item is NOT a raw material or the byproduct dict:
                itemRecipe = findItemRecipe(dictionary)
                machineName = itemRecipe["machine"] #access the key "machine" in the individual recipe dictionary to get the name of the machine.
                line1 = separator + dictionary["name"].title() + "\n\n" #Name of product
                if machineName:
                    line2 = str(dictionary["numOfMachines"]) + " " + machineName.title() #Number of machines needed....
                    totalNumMachines[machineName] += dictionary["numOfMachines"]
                    if dictionary["numOfMachines"] != 1:
                        if machineName.title() == "Oil Refinery":
                            line2 = line2[:(len(line2)-1)]
                            line2 += "ies" #grammar
                        else:
                            line2 += "s" #grammar
                
                line2 += " needed to produce " + str(fTruncate(dictionary["baseProductionRate"] * proliferatorBonus[proliferatorLevel] * timeUnitModifier[timeUnit])) + " per " + timeUnit #.... to produce x items per time unit (seconds, minutes, hours)
                line3 = "\n" #newline
                entry = line1 + line2 + line3 #add the lines together
                
                for ingredient, amount in dictionary.items(): #for every key in dictionary, check to see if it's an item, if yes, make "Needs x ingredient per time unit" and then add to the entry variable
                    if ingredient in recipeDictionary:
                        lineX = "\nNeeds " + str(fTruncate(amount * timeUnitModifier[timeUnit])) + " " + ingredient.title() + " per " + timeUnit
                        entry += lineX
            
                finishedResults += entry #add each finished formatted entry to a string that'll be written to a text document
                overallResults.pop(overallResults.index(dictionary))
        
        #Byproduct section #HARDCODED FOR HYDROGEN
        for dictionary in overallResults: #find byproduct dict. should be last but to be safe, check them all. Not many left anyway
            if dictionary["name"] == "byproduct":
                byproductSection = separator + "\nByproducts:\n"
                amountOfByproduct = dictionary["producedAmount"]
                line1 = str(amountOfByproduct * timeUnitModifier[timeUnit]) + " Hydrogen per " + timeUnit
                byproductSection += line1
                overallResults.pop(overallResults.index(dictionary))
                finishedResults += byproductSection
        
        machineSection = separator + "\nManufacturing Facilities:\n"
        for machine, number in totalNumMachines.items(): # total number of machines needed
            line = str(number) + " " + machine.title()
            if number != 1:
                if machine == "oil refinery":
                    line = str(number) + " Oil Refinerie" #the 's' gets added below, this is not a typo.
                line += "s"
            machineSection += line + "\n"
            
        finishedResults += machineSection
        
        rawMaterialSection = "\nRAW MATERIALS:\n"
        for rawMatDict in overallResults:
            line = str(fTruncate(rawMatDict["baseProductionRate"] * proliferatorBonus[proliferatorLevel] * timeUnitModifier[timeUnit])) + " " + rawMatDict["name"].title() + " per " + timeUnit + "\n"
            rawMaterialSection += line
            
        finishedResults += rawMaterialSection
        
        return finishedResults
            
            #DONE - Would be nice to have a function for adding more recipes to recipeDictionary in the future.
            #DONE - Also, need to create the UI. Maybe make an "ascii art" ui and clear the terminal everytime you alter something and then redisplay the ui with the changes made.
            #DONE - Also, need to be able to use advanced recipes.
            #DONE - ASCII Art of the DSP logo
            #DONE - add way to change time unit
            #TEMPORARILY NOT IMPLEMENTED - (need to come up with a good way of sorting the results. This does not work. -->) Sort "overallResults" before formatting works it's magic. Sort by baseProductionRate least to greatest first, then sort duplicates by number of ingredients greatest to least
            #DONE - Add byproducts
            #DONE - Save settings
            
            #Global variables that need to be created:
            #DONE - recipeDictionary - A dictionary of dictionaries. item names are keys and the dictionaries are recipes.
            #DEPRECATED - overallResults - a list of all the calculations made above. Initialized as an empty list. DEPRECATED. Functions now return overallResults as a value, rather than relying on modifying a global variable
            #DONE - endToStartResults - same purpose as overallResults. It's a global variable because it needs to survive the recursive function and not be overwritten every time. Still returned like overallResults
            #DONE - machineLevelUsed - dictionary with every machine as keys and the level being used in the calculations as values.
            #DONE - machineSpeedDictionary - machine levels as keys, machine production speeds as values
            #DONE - timeUnit
            #DONE - proliferatorBonus
            #DONE - timeUnitModifier
            
def fTruncate(floatNum, numOfDigits=1):
    truncatedFloat = int(floatNum * (10**numOfDigits))/(10**numOfDigits)
    return float(truncatedFloat)

#User interaction part

## BLESSED Less comments from here on out because I don't have a clue what I'm doing and I want to get the code written down before I forget how to write it.
#Terminal height is 30, terminal width is 120
term = blessed.Terminal()

mainMenuList = ["Calculator", "Change Machine Level Used", "Change Rare Materials Available", "Change Time Unit", "Credits", "Quit"]
creditsList = ["u/FactoryBuilder", "   -> Creator \n           -> Lead Python Programmer \n           -> Head of the Art Department", 
               " ", 
               "Blessed. https//:blessed.readthedocs.org", 
               "   -> Copyright (c) 2014 Jeff Quast", 
               "   -> Copyright (c) 2011 Erik Rose", 
               "    Blessed, the Python terminal application library, \n            was used with permission as outlined\n            in the MIT license.", 
               " ", 
               "Dyson Sphere Program", 
               "   -> Created by Youthcat Studio", 
               "   -> The game for which this program\n              is intended to be used for."]
currentOptionList = mainMenuList
background = term.on_lightblue
alternate = -1
currentLocation = (0,0)
currentSelection = 1
longestMachineName = 1
longestRareMatName = 1
timeUnitSelectionArrow = (term.green + "  <<<")
timeList = []
exitKeys = ["KEY_ESCAPE", "KEY_BACKSPACE", "KEY_ENTER"]
asciiArtDSPLogo = [
"                                                   __          ",
"                                                _,/ /          ",
"                                              _/,_ /           ",
"                     ____,-M\-----.___     _/’,/M /            ",
"                 _,-!!!!!!!!M\        ‘-’’’ ,/M/,/             ",
"              ,-’!!!!!!!!!!!|M|______     _/M/ /               ",
"            ,/!\M\!!!!!!!!MMMMMMMMMM‘-./’M/  ‘._               ",
"          ,/!!!!!\MM!!!’MMMMMMMMMMMMMMMMM,/      \             ",
"         /!!!!!!!!!!‘MMMMMMMMMMMMMMMMMMM/         \            ",
"        /!!!!!!!!!!!MMMMMMMMMMMMMMMMMM/’           ‘.          ",
"       /!!!!!!!!!!!MMMMMMMMMMMMMMMMM/’              ‘.         ",
"      /gggg!!!!!!!|MMMMMMMMMM/’   ‘’                 ‘:        ",
"     ;!!!!!PPPPPPPMMMMMMMMMM|                         ‘}       ",
"     |!!!!!!!!!!!!MMMMMMMMMMM\                         ]       ",
"     |!!!!!!!!!!!!!MMMMMMMMMM/ ,,                      |       ",
"     |!!!!!!!!!!!!,MMMMMMMMP/ /MM\                     |       ",
"     {!!!!!!!!!’PPP MMMMMP/ /’MMMM\                    ]       ",
"     {!!!!!’PPP       YM/ /’MMMMMMM\                  ;        ",
"      :PPP’             ,/MMMMMMMMMM|                ;         ",
"       \               /MMMMMMMMMMMM|               ;          ",
"        \            /’MMMMMMMMMMMMM;              /           ",
"         \         /’MMMMMMMMMMMMMM/              /            ",
"          ‘.     /’MMMMMMMMMMMMMM/’             /’             ",
"            ‘\  /MMMMMMMMMMMMMM/’            _/’               ",
"            /’/M/’   \MMMMMM/             _,’                  ",
"          ,//M/’ ,-.____             __,-’                     ",
"         //M/’_/’       ‘-----------’                          ",
"        /M__/’                                                 ",
"       /,/                                                     "]


def printFunc(position: list, speech, colour, endChar='\n'):#absolute position #colour = term.colour name (ex. red)
    # COLOUR HAS TO BE BEFORE SPEECH OTHERWISE IT WON'T CHANGE THE COLOUR OF THE TEXT!
    print(term.move_xy(position[0], position[1]) + colour +  str(speech), end=endChar, flush=True)

def setup(optionList: list, spacing: int, distanceFromTop, distanceFromLeft, clear: bool=True, makeCurrent: bool=True): #sets up a list of strings
    global currentOptionList
    global currentSelection
    
    currentSelection = 1
    if clear:
        print(term.home + background + term.clear, end='') #clears screen
    current = 1
    for option in optionList: #setup
        printFunc([distanceFromTop, (current-1)*spacing + distanceFromLeft], '{}'.format(option), term.red, endChar='')
        current += 1
    
    alternate = -1 #so that it blinks quicker. w/o this, alternate could be 1 when we get back to the main menu so it wouldn't blink for 1 second instead of 0.5
    if makeCurrent:
        #distanceFromTop and distanceFromLeft are mucked up here. They're inverted and I don't want go through all my code fixing it just so it looks right. I'll just write them in reverse here.
        printFunc([(distanceFromTop-4), (distanceFromLeft + (spacing*(currentSelection-1)))], "--> {}".format(optionList[currentSelection-1]), term.green, endChar='') #highlights option 1
        currentOptionList = optionList #sets the current list as the argument list
    #DSP Logo displaying #Height of logo: 29, width of logo: 62 #6 is arbitrary. It's how far from the edge right side the logo is.
    if optionList != asciiArtDSPLogo:    
        setup(asciiArtDSPLogo, 1, term.width-58, 0, clear=False, makeCurrent=False)
    print(term.home,flush=True)

def setupAdjustmentArrows(colour=term.green,minNum=1):
    currentLocation = term.get_location()
    
    leftPossible = machineLevelUsed[currentOptionList[currentSelection-1].lower()] != minNum
    rightPossible = machineLevelUsed[currentOptionList[currentSelection-1].lower()] < machineMaxLevel[currentOptionList[currentSelection-1].lower()]
    
    leftChar = ' '
    rightChar = ' '
    
    if leftPossible:
        leftChar = '<'
    if rightPossible:
        rightChar = '>'
    
    printFunc([8 + longestMachineName + 3, currentLocation[0]], leftChar, colour, endChar='') #left arrow
    printFunc([8 + longestMachineName + 5, currentLocation[0]], rightChar, colour, endChar='') #right arrow
    
    return [leftPossible, rightPossible]

def textModeFunc(prompt='', startPosition: list=[0, 0]): #by default it (should) return home
    textString = ''
    print(term.move_xy(startPosition[0], startPosition[1]), end='', flush=True)
    print(prompt, end='', flush=True)
    while True:
        keyInput = term.inkey()
        if keyInput.is_sequence == False:
            textString += keyInput
            print(term.move_xy(startPosition[0], startPosition[1]), end='')
            print("{0}{1}".format(prompt,textString), end='', flush=True)
        if keyInput.name == "KEY_BACKSPACE":
            textString = textString[:len(textString)-1] + ' '
            print(term.move_xy(startPosition[0], startPosition[1]), end='')
            print("{0}{1}".format(prompt,textString), end='', flush=True)
            textString = textString.strip()
        if keyInput.name == "KEY_ENTER":
            print("",flush=True)
            return textString

def blink(overrideLocation=None): #by default, it blinks where lists normally start in the terminal: (4,2)
    global alternate                                    #override this if the options are somewhere else.
    global currentSelection
    global currentOptionList
    blinkLocation = [4,2*(currentSelection)]
    
    if overrideLocation:
        blinkLocation = overrideLocation
    
    if alternate == 1:
        printFunc(blinkLocation, "--> {}".format(currentOptionList[currentSelection-1]), term.green, endChar='')
    else:
        printFunc(blinkLocation, "    {}".format(currentOptionList[currentSelection-1]), term.green, endChar='')
    alternate *= -1

def recipeAdder():
    print(term.home + term.on_lightred + term.clear, end='')
    printFunc([2,0], "FORMAT: {}".format('"magnetic coil": {"machine": "assembling machine", "producedAmount": 2, "timeToMake": 1, "magnet": 2, "copper ingot": 1}'), term.yellow)
    name = textModeFunc("Enter name of end product: ", [2,3])
    machine = textModeFunc("Enter name of machine(press enter to default to assembling machine): ", [2,4])
    amount = textModeFunc("Enter amount produced in one recipe(press enter to default to 1): ", [2,5])
    time = textModeFunc("Enter time to make (default is 1): ", [2,6])
    if machine == "":
        machine = "assembling machine"
    if amount == "":
        amount = 1
    if time == "":
        time = 1
    
    newRecipe = [name, {"machine": machine, "producedAmount": float(amount), "timeToMake": float(time)}]
    
    numOfIngredients = textModeFunc("Enter number of unique ingredients: ", [2,7])
    for ingredient in range(int(numOfIngredients)):
        ingredientName = textModeFunc("Enter name of ingredient: ", [2,8+2*ingredient])
        ingredientNum = textModeFunc("Enter number of that ingredient needed: ", [2,9+2*ingredient])
        newRecipe[1][ingredientName] = int(ingredientNum)
    
    recipeDictionary[newRecipe[0]] = newRecipe[1] #[0] is the name, [1] is the associated dictionary, the recipe.
    
    with open(recipeDictFilepath, "w") as recipeFile:
        json.dump(recipeDictionary, recipeFile)
    

#UI PART
with term.cbreak(), term.hidden_cursor():
    keyInput = ''
    
    setup(mainMenuList, 2, 8, 2)
    
    #machineList creation and longestMachineName finder
    for machine in machineLevelUsed.keys():
        machineList.append(machine.title())
        if len(machine) > longestMachineName:
            longestMachineName = len(machine)
    machineList.append("BACK") #Needs to be added to setup() so we can manually define its position, overriding the parameters given to setup() defining spacing and postioning
    
    #Ditto but for rareMats
    for rareMat in usableRareMats.keys():
        possibleRareMatsOptionsList.append(rareMat.title())
        if len(rareMat) > longestRareMatName:
            longestRareMatName = len(rareMat)
    possibleRareMatsOptionsList.extend(["ALL Yes", "ALL No", "BACK"])
    
    while True:
        keyInput = term.inkey(timeout=0.5)
        if keyInput.name == "KEY_DOWN":
            alternate = -1
            if currentSelection < len(currentOptionList):
                printFunc([4,2*currentSelection], "    {}".format(currentOptionList[currentSelection-1]), term.red, endChar='')
                printFunc([4,2*(currentSelection+1)], "--> {}".format(currentOptionList[currentSelection]), term.green, endChar='')
                currentSelection += 1
                    
        if keyInput.name == "KEY_UP":
            alternate = -1
            if currentSelection > 1: #1 is bottom of every list
                printFunc([4,2*currentSelection], "    {}".format(currentOptionList[currentSelection-1]), term.red, endChar='')
                currentSelection -= 1
                printFunc([4,2*(currentSelection)], "--> {}".format(currentOptionList[currentSelection-1]), term.green, endChar='')
                
        if keyInput.name == "KEY_HOME":
            while True: #THERE IS NO BACK. IF YOU GET INTO HERE, YOU HAVE TO QUIT THE PROGRAM. or just press enter a bunch of times and draw an error.
                recipeAdder()
            
        if not keyInput:
            if currentOptionList == ["BACK"]:
                blink([4, 26]) #overrides to blink on the back button's location in the "Credits" menu.
                                # WARNING! THIS IS NOT DYNAMIC! It functions for this one specific case and will probably break in other cases. Luckily, I'm mostly done the UI so there won't *be* any other cases.
            else:
                blink()
                
        if (keyInput.name == "KEY_ENTER") and (currentOptionList == mainMenuList): 
            match currentOptionList[currentSelection-1]:
                case "Calculator":
                    print(term.clear + background + term.red + term.home)
                    item = textModeFunc("Enter name of end product: ")
                    currentLocation = list(term.get_location())
                    currentLocation.reverse()
                    itemNum = textModeFunc("Enter number of end products per {}: ".format(timeUnit), currentLocation)
                    
                    itemDictionary = {"name": str(item), "amountPerSecond": (float(itemNum)/timeUnitModifier[timeUnit])}
                    print("\nCalculating...") #\n because lines end with ''
                    finishedResults = formatting(numMachineCalc(byproduct(endToStart(itemDictionary))))
                    
                    filename = r"results\results_" + item + str(itemNum) + "p" + timeUnit.strip('econdiutr') + ".txt" #econdiutr are the letters in "second" "minute" and "hour" that don't occur in the first position.
                    
                    resultsFilename = os.path.abspath(filename)
                    
                    with open(resultsFilename, 'w') as file: #save the results in .txt file
                        file.write(finishedResults)
                    
                    endToStartResults = []
                    
                    print("Calculated. Results outputted to file: {}".format(resultsFilename))
                    print(term.green + "\nPress Enter to return to the main menu")
                    
                    keyInput = term.inkey() #gets rid of it being ENTER
                    
                    while keyInput.name != "KEY_ENTER": #keeps the lines on screen until enter is pressed.
                        keyInput = term.inkey()
                        
                    setup(mainMenuList, 2, 8, 2)
                    
                case "Change Machine Level Used":
                    print(term.home + background + term.clear, end='') # Need to clear screen first. Then print the numbers. Then print the names. This way, the current selection option is not 3 and is instead whatever the first machine in machineList is.
                    setup(list(machineLevelUsed.values()), 2, 8 + longestMachineName + 4, 2, clear=False, makeCurrent=False)
                    setup(machineList, 2, 8, 2, clear=False)
                    
                case "Change Rare Materials Available":
                    print(term.home + background + term.clear, end='') # Need to clear screen first. Probably. Did it for machineList so I'm doing it here. It's one line of code.
                    setup(list(usableRareMats.values()), 2, 8 + longestRareMatName + 4, 2, clear=False, makeCurrent=False)
                    setup(possibleRareMatsOptionsList, 2, 8, 2, clear=False)
                    
                case "Change Time Unit":
                    timeList = []
                    for unit in list(timeUnitModifier.keys()):
                        timeList.append(unit.title() + 's')
                    timeList.append("BACK")
                    
                    spot = timeList.index(timeUnit.title() + 's')
                    unitSelect = timeList[spot] + timeUnitSelectionArrow
                    timeList.remove(timeUnit.title() + 's')
                    timeList.insert(spot, unitSelect)
                    
                    setup(timeList, 2, 8, 2)
                    
                case "Credits":
                    setup(creditsList, 2, 8, 2, makeCurrent=False)
                    setup(["BACK"], 1, 8, 26, clear=False)
                    
                case "Quit":
                    quit()
                
        elif (keyInput.name == "KEY_ENTER") and (currentOptionList == machineList):
            printFunc([4,2*(currentSelection)], "--> {}".format(currentOptionList[currentSelection-1]), term.green, endChar='')
            match currentOptionList[currentSelection-1]:
                case "BACK":
                    saveList = [timeUnit, proliferatorLevel, machineLevelUsed, usableRareMats]
                    
                    with open(configFilepath, 'w') as file:
                        json.dump(saveList, file)
                        
                    setup(mainMenuList, 2, 8, 2)
                
                case "Proliferator":
                    currentLocation = term.get_location()
                    canGoLeft, canGoRight = setupAdjustmentArrows(minNum=0)
                    printFunc([8, len(currentOptionList)*2 + 6], "                          ", term.yellow_on_lightblue, endChar='') #see the first line of the else statement under case other: to find out what this is for.
                    printFunc([8 + longestMachineName + 4, currentLocation[0]], machineLevelUsed[currentOptionList[currentSelection-1].lower()], term.green, endChar='')
                    while True:
                        keyInput = term.inkey(timeout=0.25)
                        if (keyInput.name == "KEY_LEFT") and (canGoLeft):
                            machineLevelUsed[currentOptionList[currentSelection-1].lower()] -= 1
                            canGoLeft, canGoRight = setupAdjustmentArrows(minNum=0)
                            printFunc([8 + longestMachineName + 4, currentLocation[0]], machineLevelUsed[currentOptionList[currentSelection-1].lower()], term.red, endChar='')
                            alternate = 1
                            #go left decrease by 1
                        elif (keyInput.name == "KEY_RIGHT") and (canGoRight):
                            machineLevelUsed[currentOptionList[currentSelection-1].lower()] += 1
                            canGoLeft, canGoRight = setupAdjustmentArrows(minNum=0)
                            printFunc([8 + longestMachineName + 4, currentLocation[0]], machineLevelUsed[currentOptionList[currentSelection-1].lower()], term.red, endChar='')
                            alternate = 1
                            #go right increase by 1
                        elif not keyInput:
                            if alternate == 1:
                                printFunc([8 + longestMachineName + 4, currentLocation[0]], machineLevelUsed[currentOptionList[currentSelection-1].lower()], term.green, endChar='')
                            else:
                                printFunc([8 + longestMachineName + 4, currentLocation[0]], machineLevelUsed[currentOptionList[currentSelection-1].lower()], term.red, endChar='')
                            alternate *= -1
                        elif keyInput.name in exitKeys:
                            printFunc([8 + longestMachineName + 3, currentLocation[0]], " {} ".format(machineLevelUsed[currentOptionList[currentSelection-1].lower()]), term.red, endChar='')
                            proliferatorLevel = list(proliferatorBonus.keys())[machineLevelUsed[currentOptionList[currentSelection-1].lower()]]
                            break
                
                case other:
                    currentLocation = term.get_location()
                    canGoLeft, canGoRight = setupAdjustmentArrows()
                    
                    if machineMaxLevel[currentOptionList[currentSelection-1].lower()] == 1:
                        printFunc([8, len(currentOptionList)*2 + 6], "No other levels available!", term.yellow_on_black, endChar='')
                        print(background,flush=True)
                    else:
                        printFunc([8, len(currentOptionList)*2 + 6], "                          ", term.yellow_on_lightblue, endChar='') #erases the above message if it exists.
                        printFunc([8 + longestMachineName + 4, currentLocation[0]], machineLevelUsed[currentOptionList[currentSelection-1].lower()], term.green, endChar='')
                        while True:
                            keyInput = term.inkey(timeout=0.25)
                            if (keyInput.name == "KEY_LEFT") and (canGoLeft):
                                machineLevelUsed[currentOptionList[currentSelection-1].lower()] -= 1
                                canGoLeft, canGoRight = setupAdjustmentArrows()
                                printFunc([8 + longestMachineName + 4, currentLocation[0]], machineLevelUsed[currentOptionList[currentSelection-1].lower()], term.red, endChar='')
                                alternate = 1
                                #go left decrease by 1
                            elif (keyInput.name == "KEY_RIGHT") and (canGoRight):
                                machineLevelUsed[currentOptionList[currentSelection-1].lower()] += 1
                                canGoLeft, canGoRight = setupAdjustmentArrows()
                                printFunc([8 + longestMachineName + 4, currentLocation[0]], machineLevelUsed[currentOptionList[currentSelection-1].lower()], term.red, endChar='')
                                alternate = 1
                                #go right increase by 1
                            elif not keyInput:
                                if alternate == 1:
                                    printFunc([8 + longestMachineName + 4, currentLocation[0]], machineLevelUsed[currentOptionList[currentSelection-1].lower()], term.green, endChar='')
                                else:
                                    printFunc([8 + longestMachineName + 4, currentLocation[0]], machineLevelUsed[currentOptionList[currentSelection-1].lower()], term.red, endChar='')
                                alternate *= -1
                            elif keyInput.name in exitKeys:
                                printFunc([8 + longestMachineName + 3, currentLocation[0]], " {} ".format(machineLevelUsed[currentOptionList[currentSelection-1].lower()]), term.red, endChar='')
                                break
        
        elif (keyInput.name == "KEY_ENTER") and (currentOptionList == possibleRareMatsOptionsList):
            printFunc([4,2*(currentSelection)], "--> {}".format(currentOptionList[currentSelection-1]), term.green, endChar='')
            match currentOptionList[currentSelection-1]:
                case "BACK":
                    saveList = [timeUnit, proliferatorLevel, machineLevelUsed, usableRareMats]
                    
                    with open(configFilepath, 'w') as file:
                        json.dump(saveList, file)
                        
                    setup(mainMenuList, 2, 8, 2)
                case "ALL Yes":
                    for rareMat in usableRareMats.keys():
                        usableRareMats[rareMat] = 'Y' #Make all options Y
                    setup(list(usableRareMats.values()), 2, 8 + longestRareMatName + 4, 2, clear=False, makeCurrent=False) #Rewrite the letters
                    currentSelection = currentOptionList.index("ALL Yes") + 1 #setup() makes currentSelection = 1 so this line overrides that and makes currentSelection "ALL Yes"
                    printFunc([4,2*(1)], "    {}".format(currentOptionList[0]), term.red, endChar='') #Rewrite the first option in the list because otherwise it gets messed up #In the position argument, it says [4,2*(1)]. 1 is the first selection. Normally it would be "currentSelection" but we don't want to rewrite the current selection. We want the first option
                case "ALL No":
                    for rareMat in usableRareMats.keys(): #Make all options N
                        usableRareMats[rareMat] = 'N'
                    setup(list(usableRareMats.values()), 2, 8 + longestRareMatName + 4, 2, clear=False, makeCurrent=False) #Rewrite the letters
                    currentSelection = currentOptionList.index("ALL No") + 1 #setup() makes currentSelection = 1 so this line overrides that and makes currentSelection "ALL No"
                    printFunc([4,2*(1)], "    {}".format(currentOptionList[0]), term.red, endChar='') #Rewrite the first option in the list because otherwise it gets messed up #In the position argument, it says [4,2*(1)]. 1 is the first selection. Normally it would be "currentSelection" but we don't want to rewrite the current selection. We want the first option
                case other: #Essentially the same as "ALL Yes", and "ALL No" except we just do it for one instead of all.
                    if usableRareMats[currentOptionList[currentSelection-1].lower()] == 'Y': #If Y, change to N
                        usableRareMats[currentOptionList[currentSelection-1].lower()] = 'N'
                    else: #Otherwise, it has to be N so make it Y
                        usableRareMats[currentOptionList[currentSelection-1].lower()] = 'Y'
                    tempMem = currentOptionList.index(currentOptionList[currentSelection-1]) + 1 #holds the current selection in memory for a sec so that after setup defaults to currentSelection = 1, we can override with whatever we were on before. #tempMem stands for 'temporary memory'
                    setup(list(usableRareMats.values()), 2, 8 + longestRareMatName + 4, 2, clear=False, makeCurrent=False) #Rewrite the letters
                    currentSelection = tempMem #setup() makes currentSelection = 1 so this line overrides that and makes currentSelection whatever we were just selecting
                    printFunc([4,2*(currentSelection)], "--> {}".format(currentOptionList[currentSelection-1]), term.green, endChar='')
                    if currentSelection != 1:
                        printFunc([4,2*(1)], "    {}".format(currentOptionList[0]), term.red, endChar='') #Rewrite the first option in the list because otherwise it gets messed up #In the position argument, it says [4,2*(1)]. 1 is the first selection. Normally it would be "currentSelection" but we don't want to rewrite the current selection. We want the first option

        elif (keyInput.name == "KEY_ENTER") and (currentOptionList == timeList):
            printFunc([4,2*(currentSelection)], "--> {}".format(currentOptionList[currentSelection-1]), term.green, endChar='')
            match currentOptionList[currentSelection-1]:
                case "BACK":
                    saveList = [timeUnit, proliferatorLevel, machineLevelUsed, usableRareMats]
                    
                    with open(configFilepath, 'w') as file:
                        json.dump(saveList, file)
                        
                    setup(mainMenuList, 2, 8, 2)
                case other:
                    unitPicked = currentOptionList[currentSelection-1]
                    sliceSpotDict = {"S": 6, "M": 6, "H": 4}
                    firstLetter = unitPicked[:1]
                    
                    unitPicked = (unitPicked[:sliceSpotDict[firstLetter]]).lower()
                    timeUnit = unitPicked
                    
                    timeList = []
                    for unit in list(timeUnitModifier.keys()):
                        timeList.append(unit.title() + 's')
                    timeList.append("BACK")
                    
                    spot = timeList.index(unitPicked.title() + 's')
                    unitSelect = timeList[spot] + timeUnitSelectionArrow
                    timeList.remove(unitPicked.title() + 's')
                    timeList.insert(spot, unitSelect)
                    
                    tempMem = currentOptionList.index(currentOptionList[currentSelection-1]) + 1
                    setup(timeList, 2, 8, 2)
                    currentSelection = tempMem #setup() makes currentSelection = 1 so this line overrides that and makes currentSelection whatever we were just selecting
                    printFunc([4,2*(currentSelection)], "--> {}".format(currentOptionList[currentSelection-1]), term.green, endChar='')
                    if currentSelection != 1:
                        printFunc([4,2*(1)], "    {}".format(currentOptionList[0]), term.red, endChar='') #Rewrite the first option in the list because otherwise it gets messed up #In the position argument, it says [4,2*(1)]. 1 is the first selection. Normally it would be "currentSelection" but we don't want to rewrite the current selection. We want the first option
                    
        elif (keyInput.name == "KEY_ENTER") and (currentOptionList == ["BACK"]): #FOR 'Credits' OPTION! "BACK" is the only available selectable option. We need to display some text that shouldn't be selectable, only "BACK" is selectable.
            printFunc([4,2*(currentSelection)], "--> {}".format(currentOptionList[currentSelection-1]), term.green, endChar='')
            match currentOptionList[currentSelection-1]:
                case "BACK":
                    setup(mainMenuList, 2, 8, 2)

##\BLESSED



#MIT License

#Copyright 2023 u/FactoryBuilder

#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.