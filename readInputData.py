import re
import numpy as np

def readData():
    with open("NEWAISearchfile012.txt", "r") as file:
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

def algorithm(cities):
    print("hi")

    
def printData(tour, lengthOfTour):
    print("NAME = <string = >")
    print("TOURSIZE  = %d" % (len(tour)))
    print("LENGTH = %d" % (lengthOfTour))
    print(tour)
    

cities = readData()
algorithm(cities)

    
