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
# ROUTINES TO CREATE INITIAL TOUR
# ---
def genInitialTour():
    tour = list(range(1, cities.shape[0] + 1))
    rand.shuffle(tour)
    tour.append(tour[0])
    return tour


# ---
# ROUTINES TO CREATE INITIAL TOUR
# ---
def genNewTour(tour):
    currentTour = tour[:]
    randomNo = rand.sample(range(0, len(currentTour) - 1), 2)
    tempCity = currentTour[randomNo[0]]
    currentTour[randomNo[0]] = currentTour[randomNo[1]]
    currentTour[randomNo[1]] = tempCity

    if(randomNo[0] == 0) or (randomNo[1] == 0):
        currentTour[len(currentTour) - 1] = currentTour[0]
    if(randomNo[0] == len(currentTour) - 1) or (randomNo[1] == len(currentTour) - 1):
        currentTour[0] == currentTour[len(tour) - 1]
    return currentTour


# ---
# ROUTINES TO CALCULATE CHANGE IN COST BETWEEN TWO TOURS
# ---
def calculateChangeInCost(tour, newTour, cities):
    lengthofTour = getTourDistance(tour, cities)
    lengthofNewTour = getTourDistance(newTour, cities)
    changeInCost = (lengthofNewTour - lengthofTour) / lengthofTour
    return changeInCost


# ---
# ROUTINES TO CALCULATE PROBABILITY OF ASSIGNING S = S'
# ---
def calculateProbability(coolingConstant, temperature):
    result = math.exp((-coolingConstant)/temperature)
    return result


def simulatedAnnealing(cities, coolingConstant, temp):
    tour = genInitialTour()

    previousBestTour = []
    previousBestScore = 0

    currentBestTour = tour
    currentBestScore = getTourDistance(tour, cities)

    print("SIMULATED ANNEALING ===")
    printData(currentBestTour, currentBestScore)
    
    count = 1
    
    while(temp > 0.00001):
        newTour = genNewTour(tour)
    
        changeInCost = calculateChangeInCost(tour, newTour, cities)
        if(changeInCost <= 0):
            tour = newTour
        else:
            probability = calculateProbability(changeInCost, temp)
            temp = coolingConstant * temp
            if(rand.random() < probability):
                tour = newTour

        if(getTourDistance(tour, cities) <= currentBestScore):
            currentBestScore = getTourDistance(tour, cities)
            currentBestTour = tour
            
        count += 1
        
        if(count == 50000):
            if(currentBestScore == previousBestScore):
                print("Result not changing")
                break
            else:
                previousBestScore = currentBestScore
                previousBestTour = currentBestTour
                count = 1
    
    printData(currentBestTour, currentBestScore)
    saveData(currentBestTour, currentBestScore)







def saveData(currentBestTour, currentBestScore):
    file = open(("tour" + fileName + ".txt"), "w+")
    file.write("NAME = " +   fileName + ",")
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

#Parameters: cities, cooling constant, initial temperature
simulatedAnnealing(cities, 0.9999, 10)
print("--- %s seconds ---" % (time.time() - start_time))


    
