import operator
import matplotlib.pyplot as plt


def plot(points, path, cost, type):
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    
    y = list(map(operator.sub, [max(y) for i in range(len(points))], y))
    plt.plot(x, y, 'co')
    plt.figtext(0.5,0.95, ("Total Distance: ", cost), ha="center", va="center", fontsize=18, bbox={"facecolor":"r", "alpha":0.5})    
    plt.xlabel('X', fontsize = 15)
    plt.ylabel('Y', fontsize = 15)

    for _ in range(1, len(path)):
        i = path[_ - 1]
        j = path[_]
        plt.arrow(x[i], y[i], x[j] - x[i], y[j] - y[i], color='r', length_includes_head=True)
    plt.show()

def plot_points(points):
    x = []
    y = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
    plt.plot(x, y, 'co')
    plt.xlim(0, max(x) * 1.1)
    plt.ylim(0, max(y) * 1.1)
    plt.show()



