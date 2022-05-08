import numpy as np
from numpy import inf
from ant import Ant
from cities import Cities

class AS(object):    
    """
    m:          # of ants
    n:          # of cities
    alpha:      pheromone factor, exploitation, increasing leads to too many options
    beta:       visibility factor (weight of distances), exploratin, more can lead o slow or no convergence
    rho:        evaporation rate
    iterations: # of iterations to run
    antPaths:   the paths of the ants. 1 more than # of cities to return to start city
    Q:          constant for determining pheromone difference
    
    """      
    #Constructor to set parameters
    def __init__(self, n_ants: int, n_cities: int, a: float, b: float, evap: float, iter: int):

        self.m = n_ants         # of ants to search with
        self.n = n_cities       #number of cities in graph
        self.alpha = a          #pheromone factor, exploitation, lead to too many options
        self.beta = b           #visibility fator, exploration, more can lead to slow or no convergence        
        self.rho = evap         #evap rate
        self.iterations = iter  #number of iterations
        self.antPaths = np.zeros((self.m,self.n+1))     #one extra city to get back to start city.
        self.q = 1

    # Function for updating the pheromone value.
    # This will globally update at the end of each tour for ALL ants
    def updatePheromone(self, cities: Cities, ants: list):
        for i, row in enumerate(cities.pheromone):
            for j, col in enumerate(row):
                cities.pheromone[i][j] *= (1-self.rho)
                for ant in ants:
                    cities.pheromone[i][j] += ant.pd[i][j]

    # Ant colony solver.
    def solveAS(self, cities: Cities):
        minCost = inf
        bestSolution= []
        for iter in range(self.iterations):
            ants = [Ant(cities,self.alpha, self.beta) for i in range(self.m)]            # Creates array of ants
            for ant in ants:            
                for i in range(cities.numCities-1):                     # Choose next city for every ant
                    ant.chooseNextAS()
                ant.pathCost += cities.cost_matrix[ant.path[-1]][ant.path[0]]   # Adds cost of last city back to start city
                if ant.pathCost < minCost:
                    minCost = ant.pathCost
                    bestSolution = [] + ant.path 
                ant.updatePD()
            self.updatePheromone(cities, ants)
        
        bestSolution.append(bestSolution[0])        # Appends start city onto the path 
        cities.resetPheromones()
        return bestSolution, minCost


