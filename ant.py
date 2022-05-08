import numpy as np
import random
from cities import Cities
from numpy import inf, NINF


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

    def __init__(self, cities: Cities, a: float, b: float):
        self.cities = cities
        self.alpha = a
        self.beta = b
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

    # Method for choosing a random probability
    def rouletteWheel(self, p: list):
        # 1. Calculate sum of all probs
        sumP = 0
        for i in range(self.size):
            sumP += p[i]

        p_norm = np.zeros(self.size)
        probCumulative = np.zeros(self.size)
        curCumulative = 0

        # 2. Normalize the probs
        # 3. Store cumulative prob for those norms.
        for i in range(self.size):
            p_norm[i] = p[i]/sumP
            curCumulative += p_norm[i]
            probCumulative[i] = curCumulative
        
        # 4. Generate random value 
        randNum = np.random.random_sample()

        i = 0
        for p in probCumulative:
            if randNum < p:
                nextCity = i
                break
            else:
                i+=1
        return nextCity

    # Transition function for Ant System Algorithm
    def chooseNextAS(self):

        p = np.zeros(self.size)         # p is the set of probabilities to the unvisited cities
        sumDenom = 0                    # The sum for the denominator 

        # Calculating the sum for the denominator
        for i in self.unvisited:
            sumDenom += ((self.cities.pheromone[self.current][i] ** self.alpha) 
                    * (self.dist[self.current][i] ** self.beta))

        # Determining probabilities from current city to all unvisited cities.        
        for i in range(self.size):
            try:
                self.unvisited.index(i)
                numer = ((self.cities.pheromone[self.current][i] ** self.alpha) 
                    * (self.dist[self.current][i] ** self.beta))
                p[i] = numer/sumDenom
            except ValueError:
                pass

        nextCity = self.rouletteWheel(p)
        self.unvisited.remove(nextCity)     # Removes next city from unvisited
        self.path.append(nextCity)          # Adds next city to the ant's path
        self.pathCost += self.cities.cost_matrix[self.current][nextCity]    # Updating path cost
        self.current = nextCity             # Updating current city to the next city
    
    # Transition function for Ant Colony System
    def chooseNextACS(self):

        q = np.random.random_sample()   #random number 0 - 1
        p = np.zeros(self.size)         # p is the set of probabilities to the unvisited cities
        sumDenom = 0                    # The sum for the denominator
        argMax = NINF
        s = 0

        # Calculating the sum for the denominator
        for i in self.unvisited:
            sumDenom += ((self.cities.pheromone[self.current][i] ** self.alpha) 
                    * (self.dist[self.current][i] ** self.beta))

        # Determining probabilities from current city to all unvisited cities.   
        # Also Determining max of exploitation rule.     
        for i in range(self.size):
            try:
                self.unvisited.index(i)
                numer = ((self.cities.pheromone[self.current][i] ** self.alpha) 
                    * (self.dist[self.current][i] ** self.beta))
                p[i] = numer/sumDenom
                
                #Calculating arg max for ACS
                v =  (self.cities.pheromone[self.current][i]) * (self.dist[self.current][i] ** self.beta) #equation here 
                if v > argMax:
                    s = i
                    edge = (self.current, i)
                    argMax = v                   
            except ValueError:
                pass

        # if max of exploitation rule is >= randNum, then next city is that s
        if q <= argMax:
            nextCity = s        
        # Otherwise using same rule as AS
        else:
            nextCity = self. rouletteWheel(p)  

        self.unvisited.remove(nextCity)     # Removes next city from unvisited
        self.path.append(nextCity)          # Adds next city to the ant's path
        self.pathCost += self.cities.cost_matrix[self.current][nextCity]    # Updating path cost
        self.current = nextCity             # Updating current city to the next city
        return edge

    # Updating all the pheromone deltas.
    def updatePD(self):
        self.pd = np.zeros([self.size, self.size])          # Setting pd to 2d array of 0's
        for k in range(1, len(self.path)):                  # Starting at 1 because we subtract 1 
            i = self.path[k - 1]                            # Finding previous city index
            j = self.path[k]                                # Finding next city index
            self.pd[i][j] = 1/ self.pathCost
