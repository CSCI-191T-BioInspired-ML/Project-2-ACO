import numpy as np
from numpy import inf
import random
from cities import Cities

class ACO(object):    
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
    #This is the default constructor
    def __init__(self):
        self.m = 25        
        self.n = 50      
        self.alpha = 1.7          
        self.beta = 1.7            
        self.rho = 0.2         
        self.iterations = 150  
        self.antPaths = np.zeros((self.m,self.n+1))     
        self.Q = 1          

    #Constructor to set parameters yourself
    # def __init__(self, n_ants: int, n_cities: int, iter: int, a: float, b: float, evap: float, Q: int):

    #     self.m = n_ants         # of ants to search with
    #     self.n = n_cities       #number of cities in graph
    #     self.alpha = a          #pheromone factor, exploitation, lead to too many options
    #     self.beta = b           #visibility fator, exploration, more can lead to slow or no convergence        
    #     self.rho = evap         #evap rate
    #     self.iterations = iter  #number of iterations
    #     self.antPaths = np.zeros((self.m,self.n+1))     #one extra city to get back to start city.
    #     self.q = Q



    def updatePheromone(self, cities: Cities, ants: list):
        for i, row in enumerate(cities.pheromone):
            for j, col in enumerate(row):
                cities.pheromone[i][j] *= self.rho
                for ant in ants:
                    ant.pd[i][j]
                    cities.pheromone[i][j] += ant.pd[i][j]


    def solveACO(self, cities: Cities):
        minCost = inf
        bestSolution= []
        for iter in range(self.iterations):
            ants = [Ant(cities,self) for i in range(self.m)]            # Creates array of ants
            for ant in ants:            
                for i in range(cities.numCities-1):                     # Choose next city for every ant
                    ant.chooseNext()
                ant.pathCost += cities.cost_matrix[ant.path[-1]][ant.path[0]]   # Adds cost of last city back to start city
                if ant.pathCost < minCost:
                    minCost = ant.pathCost
                    bestSolution = [] + ant.path 
                ant.updatePD()
            self.updatePheromone(cities, ants)
        
        bestSolution.append(bestSolution[0])        # Appends start city onto the path 
        return bestSolution, minCost


class Ant(object):
    """
    Ant object. 

    cities:         This is the graph
    colony:         The ant colony ACO
    size:           Number of cities
    path:           The path order of the ant
    pathCost:       How much the path costs up to this point
    unvisited:      The cities that are left to visit
    startCity:      The city the ant starts at, chosen randomly
    pd:             Pheromone delta list.
    current:        The current city being visited
    dist:           This is the inverse (1/distance) of the distance
    """

    def __init__(self, cities: Cities, aco: ACO):
        self.cities = cities
        self.colony = aco
        self.size = cities.numCities
        self.path = []                                      
        self.pathCost = 0                                   
        self.unvisited = [i for i in range(self.size)]      
        startCity = random.randint(0, self.size-1)          
        self.pd = []                                        
        self.path.append(startCity)                         # adds the start city to the path
        self.current = startCity                           
        self.unvisited.remove(startCity)                    # removes start city from the unvisited list
        self.dist = [[0 if i == j else 1/cities.cost_matrix[i][j] for j in range(cities.numCities)]
                    for i in range (cities.numCities)]      # sets distances to 1 of distance based on cost_matrix

    # Choosing the next city by calculating thr probabilities
    # Using the equation
    def chooseNext(self):

        p = np.zeros(self.size)         # p is the set of probabilities to the unvisited cities
        sumDenom = 0                    # The sum for the denominator 

        # Calculating the sum for the denominator
        for i in self.unvisited:
            sumDenom += ((self.cities.pheromone[self.current][i] ** self.colony.alpha) 
                    * (self.dist[self.current][i] ** self.colony.beta))

        # Determining probabilities from current city to all unvisited cities.        
        for i in range(self.size):
            try:
                self.unvisited.index(i)
                numer = ((self.cities.pheromone[self.current][i] ** self.colony.alpha) 
                    * (self.dist[self.current][i] ** self.colony.beta))
                p[i] = numer/sumDenom
            except ValueError:
                pass

        # Use probabilities to choose the next city
        # What do you guys think of this random aspect? 
        # Should it be changed???
        nextCity = 0
        randNum = random.random()     
        for i, prob in enumerate(p):    
            randNum -= prob
            if randNum <= 0:            
                nextCity = i
                break
        
        self.unvisited.remove(nextCity)     # Removes next city from unvisited
        self.path.append(nextCity)          # Adds next city to the ant's path
        self.pathCost += self.cities.cost_matrix[self.current][nextCity]    # Updating path cost
        self.current = nextCity             # Updating current city to the next city

    # Updating all the pheromone deltas.
    def updatePD(self):
        self.pd = np.zeros([self.size, self.size])          # Setting pd to 2d array of 0's
        for k in range(1, len(self.path)):                  # Starting at 1 because we subtract 1 
            i = self.path[k - 1]                            # Finding previous city index
            j = self.path[k]                                # Finding next city index

            # PD is contsant Q divided by current path cost
            self.pd[i][j] = self.colony.Q / self.pathCost
