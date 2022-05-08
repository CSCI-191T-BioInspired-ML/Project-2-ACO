#Ant Colony System 

import numpy as np
from numpy import inf, NINF
import random
from cities import Cities
from ant import Ant

class ACS(object):    
    """
    m:          # of ants
    n:          # of cities
    alpha:      pheromone factor, exploitation, increasing leads to too many options
    beta:       visibility factor (weight of distances), exploratin, more can lead o slow or no convergence
    rho:        evaporation rate
    iterations: # of iterations to run
    antPaths:   the paths of the ants. 1 more than # of cities to return to start city
    Q:          constant for determining pheromone difference
    Trail:      value used for local update
    
    """
    # Constructor to set parameters 
    def __init__(self, n_ants: int, n_cities: int, a: float, b: float, evap: float, iter: int):

        self.m = n_ants         # of ants to search with
        self.n = n_cities       #number of cities in graph
        self.alpha = a          #pheromone factor, exploitation, lead to too many options
        self.beta = b           #visibility fator, exploration, more can lead to slow or no convergence        
        self.rho = evap         #evap rate
        self.iterations = iter  #number of iterations
        self.antPaths = np.zeros((self.m,self.n+1))     #one extra city to get back to start city.
        self.q = 1
        self.trail = 0.01   


    # Local update rule to ACS ---------------------------------------------------------
    def updatePheromoneGlobal(self, cities: Cities, ant):
        for i, row in enumerate(cities.pheromone):
            for j, col in enumerate(row):
                cities.pheromone[i][j] *= (1-self.rho)
                cities.pheromone[i][j] += ant.pd[i][j]

    # Local pheromone update that happens after an ant visits an edge
    def updatePheromoneLocal(self, cities: Cities, ant, edge):
        i = edge[0]
        j = edge[1]
        cities.pheromone[i][j] = (1-self.rho) * cities.pheromone[i][j] + self.rho * self.trail

    def solveACS(self, cities: Cities):
        minCost = inf
        bestSolution= []
        k = 0
        bestAnt = 0
        for iter in range(self.iterations):
            ants = [Ant(cities,self.alpha, self.beta) for i in range(self.m)]            # Creates array of ants
            for ant in ants:            
                for i in range(cities.numCities-1):                     
                    edge = ant.chooseNextACS()                                     # Choosing next edge
                    self.updatePheromoneLocal(cities, ant, edge)                # Performing local update on that edge
                ant.pathCost += cities.cost_matrix[ant.path[-1]][ant.path[0]]   # Adds cost of last city back to start city
                if ant.pathCost < minCost:
                    minCost = ant.pathCost
                    bestSolution = [] + ant.path 
                    bestAnt = k
                k+=1
                ant.updatePD()
                #end for loop for ants
            ants[bestAnt].best = True
            for ant in ants:
                ant.updatePD()
        
            self.updatePheromoneGlobal(cities, ants[bestAnt]) # Only updating the pheromone of the BEST ant tour 
            k = 0
            bestAnt = 0
        
        bestSolution.append(bestSolution[0])        # Appends start city onto the path 
        return bestSolution, minCost

