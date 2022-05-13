from plot import plot_path, plot_points
from nnheuristic import NN
from antsystem import AS
from acs import ACS
from cities import Cities
import numpy as np
import time
global numCities


numCities = 50

# Change these values to test different paremters for the algorithms
ants = 10
alpha = 1
beta = 2
rho = 0.2
iterations = 500

# May need to update path of file here when testing the program -------
graph = Cities(numCities, 'Project-2-ACO-main\data2.txt')

# Creating an object for each ACO algorithm ---------------------------
antColonyACS = ACS(ants, numCities, alpha, beta, rho, iterations)
antColonyAS = AS(ants, numCities, alpha, beta, rho, iterations)

# Running the algorithm solvers ---------------------------------------
start = time.time()
pathACS, costACS = antColonyACS.solveACS(graph)
runTimeACS = time.time() - start

start = time.time()
pathAS, costAS = antColonyAS.solveAS(graph)
runTimeAS = time.time() - start

# Printing runtimes, costs, paths, and plots.
print("ACS Path Cost: ", costACS)
print()
print("AS Path Cost: ", costAS)
print()
print()
print("ACS Runtime: ", runTimeACS)
print()
print("AS Runtime: ", runTimeAS)
print()
print()
print("ACS Path: ", pathACS)
print()
print("AS Path: ", pathAS)

# Prints the resulting paths on the plots
plot_path(graph.points, pathACS, costACS, 'ACS')
plot_path(graph.points, pathAS, costAS, 'AS')
