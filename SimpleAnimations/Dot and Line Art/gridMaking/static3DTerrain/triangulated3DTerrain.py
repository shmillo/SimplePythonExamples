import numpy as np
import matplotlib.pyplot as mplt

def f(x, m, b):
    return m*x + b

fig = mplt.figure(); ax = fig.add_subplot(111, projection='3d'); colorString = 'g'

w = 4; h = 4

noiseArr = np.random.rand(w+1,h+1); print(noiseArr)

nR = w + 1; numUp = w
for i in range(numUp + 1):
    xCoords = []; yCoords = []; uZCoords = []; lZCoords = []
    for x in range(nR - i):
        y = int(f(x, 1, i))
        xCoords.append(x); yCoords.append(y); 
        uZCoords.append(noiseArr[x][y]); lZCoords.append(noiseArr[y][x]) 
    if(i != 0):
        ax.plot(yCoords, xCoords, lZCoords, color=colorString)
    ax.plot(xCoords, yCoords, uZCoords, color=colorString)

for x in range(w + 1):
    xCoords = []; yCoords = []; uZCoords = []; lZCoords = []
    for y in range(h + 1):
        xCoords.append(x); yCoords.append(y)
        uZCoords.append(noiseArr[x][y]); lZCoords.append(noiseArr[y][x])
    ax.plot(xCoords, yCoords, uZCoords, color=colorString)
    ax.plot(yCoords, xCoords, lZCoords, color=colorString)

mplt.show()
