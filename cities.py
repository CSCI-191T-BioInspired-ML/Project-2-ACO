import numpy as np
import math

class Cities(object):

    def __init__(self,size: int, file):
        self.numCities = size
        self.cities=[]
        self.points = []
        self.cost_matrix=np.zeros([size,size])
        self.cities=[]
        #self.pheromone = .1*np.ones((size,size))        #initializing pheromone matrix to 0.1
        self.pheromone =[[1 / (size * size) for j in range(size)] for i in range(size)]
        self.loadCities(file)

    #Reads city information from given filename. 
    #Stores data in cities and points.
    def loadCities(self, fileName):
        with open(fileName) as f:
            for line in f.readlines():
                city = line.split(' ')
                self.cities.append(dict(index=int(city[0]), x=int(city[1]), y=int(city[2])))
                self.points.append((int(city[1]), int(city[2])))
        self.setDistances()

    #Returns the distance between two cities. Will be stored n cost matrix
    def distance(self,city1: dict, city2: dict):
        return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)

    #Sets all the distances in the cost matrix.
    def setDistances(self):
        for i in range(self.numCities):
            for j in range(self.numCities):
                self.cost_matrix[i][j] = self.distance(self.cities[i], self.cities[j])