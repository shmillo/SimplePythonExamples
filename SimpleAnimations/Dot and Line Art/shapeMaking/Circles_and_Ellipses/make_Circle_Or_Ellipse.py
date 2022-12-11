import numpy as np
import matplotlib.pyplot as mplt

beginning = -5.0; end = -1.0 * beginning; step = 0.5
xAxis = np.arange(beginning, end, step); yAxis = np.arange(beginning, end, step); X, Y = np.meshgrid(xAxis,yAxis)

numPoints = 60.0; circleArrayX = np.zeros(int(numPoints)); circleArrayY = np.zeros(int(numPoints)); 
radialIncrement = (np.pi*2.0)/(numPoints - 1); r = 0.0
for i in range(int(numPoints)):
    rX = 1.0; rY = 2.0; xLocation = 1.0; yLocation = 5.0
    c = np.cos(r); s = np.sin(r)
    circleArrayX[i] = c*rX + xLocation
    circleArrayY[i] = s*rY + yLocation
    r += radialIncrement

mplt.plot(circleArrayX, circleArrayY); mplt.show()