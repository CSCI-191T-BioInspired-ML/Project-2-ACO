import numpy as np
import math


# Graph object for the cities of (x,y) values
# Always reads from .txt file
class Cities(object):

    # Constructor - must send filename you wish to read from
    def __init__(self,size: int, file: str):
        self.numCities = size                       
        self.points = []
        self.cost_matrix=np.zeros([size,size])
        self.pheromone = .01*np.ones((size,size))        #initializing pheromone matrix to 0.01
        self.loadCities(file)

    # Reads city information from given filename. 
    # Stores data in cities and points.
    def loadCities(self, fileName):
        with open(fileName) as file:
            for line in file.readlines():
                city = line.split(' ')
                self.points.append((int(city[0]), int(city[1])))
        self.setDistances()

    # Returns the distance between two cities. Will be stored in cost matrix
    def distance(self,city1: tuple, city2: tuple):
        return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

    # Sets all the distances in the cost matrix.
    def setDistances(self):
        for i in range(self.numCities):
            for j in range(self.numCities):
                self.cost_matrix[i][j] = self.distance(self.points[i], self.points[j])

    # Resets the oheromones values back to original
    def resetPheromones(self):
        self.pheromone = .01*np.ones((self.numCities,self.numCities))       
