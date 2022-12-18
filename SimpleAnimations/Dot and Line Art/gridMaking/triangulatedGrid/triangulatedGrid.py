import numpy as np
import matplotlib.pyplot as mplt

def f(x, m, b):
    return m*x + b

fig = mplt.figure(); ax = fig.add_subplot()
w = 4; h = 4
xAxis = np.arange(0, w + 1, 1); yAxis = np.arange(0, h + 1, 1); X, Y = np.meshgrid(xAxis, yAxis)

colorString = 'g'

nR = w + 1; numUp = w
for i in range(numUp + 1):
    xCoords = []; yCoords = []
    for x in range(nR - i):
        xCoords.append(x); yCoords.append(f(x, 1, i))
    #print(xCoords, yCoords)
    if(i != 0):
        ax.plot(yCoords, xCoords, color=colorString)
    ax.plot(xCoords, yCoords, color=colorString)

for x in range(w + 1):
    xCoords = []; yCoords = []; zCoords = []
    for y in range(h + 1):
        xCoords.append(x); yCoords.append(y); zCoords.append(np.random.rand())
    ax.plot(xCoords, yCoords, color=colorString)
    ax.plot(yCoords, xCoords, color=colorString)


mplt.show()
