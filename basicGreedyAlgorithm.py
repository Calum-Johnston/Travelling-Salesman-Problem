import re
import numpy as np

def readData():
    with open("NEWAISearchfile535.txt", "r") as file:
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

def basicGreedy(cities):
    totalLength = 0
    tour = []
    minDistance = 100
    currentCity = 1
    nextCity = 0

    tour.append(1)
    while(len(tour) < cities.shape[0]):
        for newCity in range(1, cities.shape[0] + 1):
            if(not(newCity in tour)):
                currentDistance = getDistance(currentCity, newCity, cities)
                if(currentDistance <= minDistance):
                    minDistance = getDistance(currentCity, newCity, cities)
                    nextCity = newCity
        tour.append(nextCity)
        totalLength += minDistance
        currentCity = nextCity
        minDistance = 100    
    printData(tour, totalLength)

    
def printData(tour, lengthOfTour):
    print("NAME = <string = >")
    print("TOURSIZE  = %d" % (len(tour)))
    print("LENGTH = %d" % (lengthOfTour))
    print(tour)
    

cities = readData()
basicGreedy(cities)

    
