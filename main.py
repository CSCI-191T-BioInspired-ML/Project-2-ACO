from cmath import inf
from plot import plot, plot_points
from nnheuristic import NN
from aco import ACO
from cities import Cities
global numCities

numCities = 50
graph = Cities(50, 'data1.txt')
plot_points(graph.points)
antColony = ACO()
nearestNeighbor= NN(numCities, graph)

pathACO, costACO = antColony.solveACO(graph)
pathNN, costNN = nearestNeighbor.solveNN()

print("ACO Cost: ", costACO)
print("ACO path: ", pathACO)

print()
print()

print("NN Cost: ", costNN)
print("NN path: ", pathNN)

plot(graph.points, pathACO, costACO, 'ACO')
plot(graph.points, pathNN, costNN, 'NN')
