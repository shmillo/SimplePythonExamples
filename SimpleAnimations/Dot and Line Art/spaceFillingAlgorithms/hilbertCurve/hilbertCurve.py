import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

def Hilbert(i):
    global points, order

    index = i&3
    v = np.array(points[index])
    for j in range(1, order):
        i = i >> 2
        index = i&3
        len = 2**j
        if(index == 0):
            temp = v[0]; v[0] = v[1]; v[1] = temp
        elif(index == 1):
            v[1] += len
        elif(index == 2):
            v[0] += len; v[1] += len
        elif(index == 3):
            temp = len - 1 - v[0]
            v[0] = len - 1 - v[1]
            v[1] = temp; v[0] += len
    return v;  

fig, ax = mplt.subplots(1)

order = 4; N = int(2**order); total = N**2
points = np.zeros([4, 2]); points[0] = [0, 0]; points[1] = [0, 1]; points[2] = [1, 1]; points[3] = [1, 0]

width = 1; heighth = 1; len = width / N
xAxis = np.arange(100); yAxis = np.arange(100); X, Y = np.meshgrid(xAxis, yAxis)

path = np.zeros([total, 2]); xCoords = []; yCoords = []
for i in range(total):
    path[i] = Hilbert(i)
    xCoords.append(path[i][0]); yCoords.append(path[i][1])

ax.plot(xCoords, yCoords)
mplt.show()