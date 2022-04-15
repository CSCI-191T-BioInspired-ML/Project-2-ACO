#Nearest neighbor heuristic
import numpy as np
from numpy import inf
from cities import Cities

class NN(object):

    def __init__(self, size: int, graph: Cities):
        self.cities = graph
        self.numCities = size
        self.bestPath = []
        self.bestCost = inf

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

    def solveForCity(self, start: int):
        visited=np.zeros(self.numCities)
        path = []
        cost = 0
        (curCost, curPath) = self.nearestNeighbor(start, self.cities, visited, path, cost)
        return (curCost, curPath)


    def minEdge(self, cost_matrix, startIndex, visited):
        minEdge = inf
        edgeIndex = 0
        for i in range(self.numCities):
            curEdge = cost_matrix[startIndex][i]
            if curEdge != 0:
                if curEdge < minEdge and visited[i]==0:
                    minEdge = curEdge
                    edgeIndex = i

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
