import numpy as np
import pylab as pl
import matplotlib.pyplot as mplt

def zF(x, y): 
    return x**2.0 + y**2.0

def mesh1D(start, stop, step):
    grid = []; 
    x = start; nSteps = int((stop+step - start)/step)
    for i in range(nSteps):
        if(x <= stop+step):
            grid.append(x); x+=step
    return grid

def mesh2D(x, y):
    gridX = [0.0]*(len(x)*len(y)); gridY = [0.0]*(len(x)*len(y))
    xIndex = 0; yIndex = 0
    for i in range(len(x)):
        for j in range(len(y)):
            gridX[xIndex] = x[i]
            gridY[yIndex] = y[j]
            yIndex += 1; xIndex += 1
    return gridX, gridY

xAxis = mesh1D(-1.0, 1.0, 0.1); yAxis = mesh1D(-1.0, 1.0, 0.1)

X, Y = mesh2D(xAxis, yAxis)

Z = [ [0.0]*len(xAxis) for _ in range(len(yAxis)) ]; #print(len(Z), len(Z[0]))
xIndex = 0; yIndex = 0
for i in range(len(xAxis)):
    for j in range(len(yAxis)):
        Z[i][j] = zF(X[xIndex], Y[yIndex])
        yIndex += 1; xIndex += 1; #print(X[xIndex],  Y[yIndex])
        
#mplt.contourf(xAxis, yAxis, Z)
#mplt.show()

im = pl.imshow(Z, cmap=pl.cm.RdBu)
pl.show()