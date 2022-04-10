from plot import plot, plot2
from nnheuristic import nearestNeighbor
import math
import numpy as np
global numCities

#Function to read the cities #, x, and y values from txt file. 
#Stores city data in dictionary cities
#Stores just x,y data in array points
def getCities(points, cities, fileName):
    with open(fileName) as f:
        for line in f.readlines():
            city = line.split(' ')
            cities.append(dict(index=int(city[0]), x=int(city[1]), y=int(city[2])))
            points.append((int(city[1]), int(city[2])))

#Returns the distance between two cities. Will be stored in cost matrix
def distance(city1: dict, city2: dict):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)

#Sets all the distances in the cost matrix.
def setDistances(cost_matrix, cities):
    for i in range(numCities):
        for j in range(numCities):
            cost_matrix[i][j] = distance(cities[i], cities[j])



numCities = 50
points = []
cities = []
cost_matrix=np.zeros([numCities,numCities])

getCities(points, cities, 'data1.txt')
setDistances(cost_matrix, cities)


print("----------------Cities--------------------------")
for i in range(numCities):   
    print(cities[i])

print()
print()
print("----------------Calling Nearest Neighbor--------------------------")
visited=np.zeros(numCities)
path=[]
nearestNeighbor(47, cost_matrix, numCities, visited, path)

print()
print()
print("---------------Path--------------------------")
print(path)

#plot2(points)
plot(points, path)
