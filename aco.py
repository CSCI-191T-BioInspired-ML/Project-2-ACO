import numpy as np
from numpy import inf
import random
from cities import Cities

class ACO(object):    
    #This is the default constructor
    def __init__(self):
        self.m = 10        # of ants to search with
        self.n = 50       #number of cities in graph
        self.alpha = 1.2          #pheromone factor, exploitation, lead to too many options
        self.beta = 1.7          #visibility fator, exploration, more can lead to slow or no convergence        
        self.rho = 0.2         #evap rate
        self.iterations = 100  #number of iterations
        self.antPaths = np.zeros((self.m,self.n+1))     #one extra city to get back to start city.
        self.q = 5   

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
                    cities.pheromone[i][j] += ant.pd[i][j]


    def solveACO(self, cities: Cities):
        minCost = inf
        bestSolution= []
        for iter in range(self.iterations):
            ants = [Ant(cities.numCities, cities,self) for i in range(self.m)]
            for ant in ants:
                for i in range(cities.numCities-1):
                    ant.chooseNext()
                ant.pathCost += cities.cost_matrix[ant.path[-1]][ant.path[0]]
                if ant.pathCost < minCost:
                    minCost = ant.pathCost
                    bestSolution = [] + ant.path
                ant.updatePD()
            self.updatePheromone(cities, ants)
        
        bestSolution.append(bestSolution[0])
        minCost += cities.cost_matrix[bestSolution[0]][bestSolution[cities.numCities-1]]
        return bestSolution, minCost


class Ant(object):
    """
    Ant object. One of these for every single ant.
    Stores the path, the visited, the start city, etc
    """

    def __init__(self, numCities: int, cities: Cities, aco: ACO):
        self.cities = cities
        self.colony = aco
        self.size = numCities
        self.path = []              #order of cities visited
        self.pathCost = 0           #cost of cities visited
        self.unvisited = [i for i in range(numCities)]    #unvisited cities that can still be visited
        startCity = random.randint(0, numCities-1)  # Sets start city to a random city
        self.pd = []                   #pheromone delta: local increase of pheromone value
        self.path.append(startCity)                 # adds the start city to the path
        self.current = startCity                    # sets the current city to the start city
        self.unvisited.remove(startCity)              # removes start city from the allowed list
        self.dist = [[0 if i == j else 1/cities.cost_matrix[i][j] for j in range(cities.numCities)]
                    for i in range (cities.numCities)]


    def chooseNext(self):
        sum = 0
        for i in self.unvisited:
            sum += self.cities.pheromone[self.current][i] ** self.colony.alpha * self.dist[self.current][i] ** self.colony.beta
        
        # p is the set of probabilities to the allowed cities (unvisited)
        p = [0 for i in range(self.cities.numCities)]
        
        for i in range(self.size):
            try:
                self.unvisited.index(i)
                p[i] = (self.cities.pheromone[self.current][i] ** self.colony.alpha * 
                    self.dist[self.current][i] ** self.colony.beta) / sum
            except ValueError:
                pass

        #use probabilities to choose the next city
        nextCity = 0
        randNum = random.random()
        for i, prob in enumerate(p):
            randNum -= prob
            if randNum <= 0:
                nextCity = i
                break
        
        self.unvisited.remove(nextCity)
        self.path.append(nextCity)
        self.pathCost += self.cities.cost_matrix[self.current][nextCity]
        self.current = nextCity


    #this updates all delta t(i,j)
    def updatePD(self):
        self.pd = [[0 for j in range(self.cities.numCities)] for i in range(self.cities.numCities)]
        for _ in range(1, len(self.path)):
            i = self.path[_ - 1]
            j = self.path[_]
            #this is contsant q/over current path cost
            self.pd[i][j] = self.colony.q / self.pathCost

