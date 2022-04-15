from plot import plot_path, plot_points
from nnheuristic import NN
from aco import ACO
from cities import Cities
global numCities

numCities = 50
graph = Cities(numCities, 'data2.txt')
plot_points(graph.points)
antColony = ACO()
nearestNeighbor= NN(numCities, graph)

pathACO, costACO = antColony.solveACO(graph)
pathNN, costNN = nearestNeighbor.solveNN()

print()
print()

print("ACO Cost: ", costACO)
print("ACO path: ", pathACO)

print()
print()

print("NN Cost: ", costNN)
print("NN path: ", pathNN)

plot_path(graph.points, pathACO, costACO, 'ACO')
plot_path(graph.points, pathNN, costNN, 'NN')
