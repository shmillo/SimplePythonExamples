import numpy as np
import pylab as pl
import matplotlib.pyplot as mplt

def indexOfValue(value, axisStart, axisStep):
    return (value - axisStart)/axisStep

def lerpGradient(value, axis, axisStep, Gradient):

    lerpValue = 0.0; 
    
    if(value < axis[0]):
        lerpValue = Gradient[0]
    elif(value > axis[-1]):
        lerpValue = Gradient[-1]

    else:

        index = indexOfValue(value, axis[0], axisStep); 
        fValue = index - int(index); 

        if(index + 1 >= len(Gradient)):
            lerpValue = Gradient[-1]
        elif(index + 1 < len(Gradient)):
            lerpValue = ((1.0 - fValue) * Gradient[int(index)]) + (fValue * Gradient[int(index) + 1])

    return lerpValue
    
def zF(x, y): 
    return (1.0 - (x**2.0 + y**3.0)) * np.exp(-(x**2.0 + y**2)/2.0)

xAxis = np.arange(-3.0, 3.0, 0.1); yAxis = np.arange(-3.0, 3.0, 0.1)

X, Y = pl.meshgrid(xAxis, yAxis); Z = zF(X, Y)
gY, gX = np.gradient(Z, xAxis, yAxis)
print(gX); print(gY)

testpoint = [-1, 1, zF(3, 1)]; 
testPathXCoordinates = []; testPathYCoordinates = []
testPathXCoordinates.append(testpoint[0]); testPathYCoordinates.append(testpoint[1])

learningRate = 0.053; errorX = 5.0; errorY = 5.0; tolerance =  0.00001
for i in range(3000):

    if(errorX > tolerance and errorY > tolerance):

        oldTestPointXCoord = testpoint[0]; 
        xDiff = (learningRate * lerpGradient(oldTestPointXCoord, gX[0], 0.1, gX[0]))
        testpoint[0] = oldTestPointXCoord + xDiff
        errorX = abs(xDiff)

        oldTestPointYCoord = testpoint[1]
        yDiff = (learningRate * lerpGradient(oldTestPointYCoord, gY[0], 0.1, gY[0]))
        testpoint[1] = oldTestPointYCoord + yDiff
        errorY = abs(yDiff)

        testpoint[2] = zF(testpoint[0], testpoint[1])

        testPathXCoordinates.append(testpoint[0]); testPathYCoordinates.append(testpoint[1])

        #errorX = abs(testpoint[0] - oldTestPointXCoord); errorY = abs(testpoint[1] - oldTestPointYCoord)
         

mplt.contourf(xAxis, yAxis, Z, alpha = 0.9, label='2D Function')
mplt.colorbar()
mplt.scatter(testPathXCoordinates, testPathYCoordinates, color='r', label='path of descent function over iterations')
mplt.legend()
mplt.show()
