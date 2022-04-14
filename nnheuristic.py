#Nearest neighbor heuristic
from matplotlib.image import composite_images
import numpy as np
from cities import Cities
import math

class NN(object):

    def __init__(self, size: int, graph: Cities):
        self.cities = graph
        self.numCities = size
        self.bestPath = []
        self.bestCost = math.inf
        self.unvisited = [i for i in range(self.numCities)]    #unvisited cities that can still be visited


    def solveNN(self):
        visited=np.zeros(self.numCities)
        path = []
        cost = 0
        for i in range(self.numCities):
            (curCost, curPath) = self.nearestNeighbor(i, self.cities, visited, path, cost)
            if curCost < self.bestCost:
                self.bestCost = curCost
                self.bestPath = curPath
            visited=np.zeros(self.numCities)
            path = []
            cost = 0
        return (self.bestPath, self.bestCost)
        # print("Cost: ", self.bestCost)
        # print("Path: ", self.bestPath)

    def minEdge(self, cost_matrix, startIndex, visited):
        minEdge = 1000000000
        edgeIndex = 0
        for i in range(self.numCities):
            curEdge = cost_matrix[startIndex][i]
            if curEdge != 0:
               # try:
                    #self.unvisited.index(i)
                if curEdge < minEdge and visited[i]==0:
                    minEdge = curEdge
                    edgeIndex = i
               # except ValueError: 
                #    pass

        return (edgeIndex, minEdge)

    def nearestNeighbor(self,curCity: int, cities: Cities, visited, path, totalD):
        #Setting the starting city to visited. 

        visited[curCity] = 1
        #Will store the order of cities visited
        path.append(curCity)

        #complete is true if all cities have been visited
        complete = np.all(visited == visited[0])
        #checking if all cities have been visited
        #if yes, append start city to the end and return the path
        if complete:
            path.append(path[0])
            totalD += cities.cost_matrix[curCity][path[0]]
            path2 = path
            return (totalD, path2)
    
        #Otherwise, find next min distance
        #Update visited 
        #call nearest neighbor with new starting city
        else:
            (minI, minCost) = self.minEdge(cities.cost_matrix, curCity, visited)
            totalD += minCost
            visited[minI] = 1
            return self.nearestNeighbor(minI, cities, visited, path, totalD)
