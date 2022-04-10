#Nearest neighbor heuristic
import numpy as np


#Returns the city index and cost *note*: not currently using the cost, can remove from return statement
#If we keep it that way 
#Before storing the next minimum distance, it checks if this city is already visited.
#If it has been visited, then it skips that one and doesnt update min
def minEdge(numCities, cost_matrix, startIndex, visited):
    minEdge = 10000000
    edgeIndex = 0
    for i in range(numCities):
        curEdge = cost_matrix[startIndex][i]
        if curEdge != 0:
            if curEdge < minEdge and visited[i] == 0:
                minEdge = curEdge
                edgeIndex = i

    return (edgeIndex, minEdge)

def nearestNeighbor(startIndex, cost_matrix, numCities, visited, path):
    #Setting the starting city to visited. 
    visited[startIndex] = 1

    #Will store the order of cities visited
    path.append(startIndex)

    #complete is true if all cities have been visited
    complete = np.all(visited == visited[0])

    #checking if all cities have been visited
    #if yes, append start city to the end and return the path
    if complete:
        path.append(path[0])
    
    #Otherwise, find next min distance
    #Update visited 
    #call nearest neighbor with new starting city
    else:
        (minI, minCost) = minEdge(numCities, cost_matrix, startIndex, visited)
        visited[minI] = 1
        nearestNeighbor(minI, cost_matrix, numCities, visited, path)






