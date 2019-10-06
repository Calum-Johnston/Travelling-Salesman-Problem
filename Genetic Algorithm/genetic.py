import re
import numpy as np
import random as rand
import math
import time

def readData():
    with open((fileName + ".txt"), "r") as file:
        next(file)  #Skips first line
        line = next(file)  #Gets number of cities

        #Creates an array of the correct size
        size = re.findall('\d+', line)
        size = int(size[0])
        cities = np.zeros(shape=(size, size))

        currentX = 1
        currentY = 2

        #Fills the array (note x and y represent 1 less than they are
        for line in file:
            currentLine = line.split(",")
            if(not line.strip()):
                continue
            if(currentY > size):
                currentX += 1
                currentY = currentX + 1
            for distance in currentLine:
                if(currentY > size):
                    continue
                if distance != "\n":
                    cities[currentX - 1][currentY - 1] = distance
                    cities[currentY - 1][currentX - 1] = distance
                    currentY += 1
        return cities






def getDistance(city1, city2, cities):
    return cities[city1 - 1][city2 - 1]

def getTourDistance(tour, cities):
    totalDistance = 0
    for i in range(0, len(tour) - 1):
        totalDistance += getDistance(tour[i], tour[i+1], cities)
    return totalDistance


# ---
# ROUTINES TO CREATE A RANDOM INITIAL POPULATION
# ---
def createPopulation(cities):
    size = cities.shape[0]
    pop = []
    for i in range(0, size * 10):
        pop.append(createRoute(size))
    return pop

def createRoute(size):
    route = list(range(1, size + 1))
    rand.shuffle(route)
    route.append(route[0])
    return route


# ---
# ROUTINES TO DETERMINE THE FITNESS OF EACH ROUTE
# ---
def fitnessOfRoutes(pop, cities):
    fitnessOfPopulation = []
    for i in range(0, len(pop)):
        fitnessOfPopulation.append(1 / getTourDistance(pop[i], cities))
    return fitnessOfPopulation


# ---
# ROUTINES TO DETERMINE THE MATING POOL
# ---

def selectMatingPool(population, fitnessOfPopulation, eliteSize):
    parents = []
    totalFitness = sum(fitnessOfPopulation)

    calculateElitePopulation(population, fitnessOfPopulation[:], eliteSize, parents)
     
    for x in range(0, len(population) - eliteSize):
        parents.append(rouletteWheelSelection(population, fitnessOfPopulation, totalFitness))
    return parents

def calculateElitePopulation(population, copyOfFitness, eliteSize, parents):
    for x in range(0, eliteSize):
        index = copyOfFitness.index(max(copyOfFitness))
        parents.append(population[index])
        copyOfFitness[index] = 0

def rouletteWheelSelection(population, fitnessOfPopulation, totalFitness):
    randomNo = 0
    randomNo = round(rand.uniform(0, totalFitness), 18)
    route = currentRouteOnWheel(randomNo, population, fitnessOfPopulation)
    return route

def currentRouteOnWheel(randomNo, population, fitnessOfPopulation):
    initialSum = 0
    count = 0
    while(initialSum < randomNo):
        initialSum += fitnessOfPopulation[count]
        if(initialSum >= randomNo):
            break;
        count += 1
    return population[count]


# ---
# ROUTINES TO BREED THE MATING POOL
# ---
def breedMatingPool(matingPool, eliteSize):
    children = []

    for x in range(0, eliteSize):
        children.append(matingPool[x])
    
    for x in range(0, len(matingPool) - eliteSize):
        children.append(breedIndividualParents(matingPool[rand.randint(0, len(matingPool) - 1)], matingPool[rand.randint(0, len(matingPool) - 1)]))
    return children

def breedIndividualParents(parent1, parent2):
    child = [None] * len(parent1)

    subStringPos1 = int(rand.random() * (len(parent1) - 1))
    subStringPos2 = int(rand.random() * (len(parent1) - 1))
    
    for x in range(min(subStringPos1, subStringPos2), max(subStringPos1, subStringPos2)):
        child[x] = parent1[x]

    count = 0
    for y in range(0, len(parent2) - 1):
        if(child[y] == None):
            while(parent2[count] in child):
                count += 1
            child[y] = parent2[count]
    child[len(parent2) - 1] = child[0]
    return child


# ---
# ROUTINES TO MUTATE THE CHILDREN PRODUCED FROM BREEDING
# ---
def mutateChildren(children, mutationProbability):
    newPopulation = []

    for x in range(0, len(children)):
        newPopulation.append(mutateChild(children[x], mutationProbability))
    return newPopulation

def mutateChild(child, mutationProbability):
    if(rand.random() < mutationProbability):
        posToMutate1 = int(rand.random() * (len(child) - 1))
        posToMutate2 = int(rand.random() * (len(child) - 1))
    
        tempCity = child[posToMutate1]
        child[posToMutate1] = child[posToMutate2]
        child[posToMutate2] = tempCity

        if(posToMutate1 == 0) or (posToMutate2 == 0):
            child[len(child) - 1] = child[0]
        if(posToMutate1 == len(child) - 1) or (posToMutate2 == len(child) - 1):
            child[0] == child[len(child) - 1]
    return child


# ---
# ROUTINES TO RUN THE WHOLE SIMULATION
# ---
def geneticAlgorithm(cities, eliteSize, mutationProbability, noOfGenerations):
    eliteSize = math.ceil((eliteSize * (cities.shape[0] + 1))/100)

    #Create the initial Population (a list of different routes)
    population = createPopulation(cities)

    print("GENETIC SEARCH ===")
    bestInitialRoute = getBestRoute(population, cities)
    printData(bestInitialRoute, getTourDistance(bestInitialRoute, cities))

    for i in range(0, noOfGenerations):
        newGeneration = createNewGeneration(population, eliteSize, mutationProbability)
        population = newGeneration

    bestFinalRoute = getBestRoute(newGeneration, cities)
    printData(bestFinalRoute, getTourDistance(bestFinalRoute, cities))
    saveData(bestFinalRoute, getTourDistance(bestFinalRoute, cities))
    
def createNewGeneration(population, eliteSize, mutationProbability):
    
    #Calculates the fitness of each route in the population
    fitnessOfPopulation = fitnessOfRoutes(population, cities)

    #Calculates which routes are to be breeded
    matingPool = selectMatingPool(population, fitnessOfPopulation, eliteSize)

    #Breeds two Parents to produce two offspring
    children = breedMatingPool(matingPool, eliteSize)

    #Mutates current population to avoid local convergence
    newPopulation = mutateChildren(children, mutationProbability)

    return newPopulation

def getBestRoute(population, cities):
    fitnessOfPopulation = fitnessOfRoutes(population, cities)
    currentBestScore = 0
    currentBestPosition = 0
    for x in range(0, len(population)):
        if(fitnessOfPopulation[x] < currentBestScore):
            currentBestScore = fitnessOfPopulation[x]
            currentBestPosition = x
    return population[currentBestPosition]







def saveData(currentBestTour, currentBestScore):
    file = open(("tour" + fileName + ".txt"), "w+")
    file.write("NAME = " + fileName + ",")
    file.write("TOURSIZE = " + str((len(currentBestTour) - 1)) + ",")
    file.write("LENGTH = " + str(int(currentBestScore)) + ",")
    for x in range(0, len(currentBestTour) - 1):
        if(x == len(currentBestTour) - 2):
            file.write(str(currentBestTour[x]))
        else:
            file.write(str(currentBestTour[x]) + ",")
    file.close()
    
def printData(tour, lengthOfTour):
    print("TOURSIZE  = %d" % (len(tour)))
    print("LENGTH = %d" % (lengthOfTour))
    print(tour)
    

	
#Enter your file name here
fileName = "Cities"
cities = readData()

#Parameters: cities, elite percent, mutation probability, generation number
geneticAlgorithm(cities, 10, 0.01, 1000)

