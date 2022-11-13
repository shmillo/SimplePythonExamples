import numpy as np
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
    return x**2.0 + y**2.0

xAxis = []; yAxis = []
start = -1.0; stop = 1.0; step = 0.253; stop = stop; numSteps = int((stop - start)/step); tempAxisValue = start
for i in range(numSteps):
    xAxis.append(tempAxisValue); yAxis.append(tempAxisValue)
    tempAxisValue = tempAxisValue + step
print(xAxis)

X, Y = np.meshgrid(xAxis, yAxis, indexing='ij'); Z = zF(X, Y); 
gY, gX = np.gradient(Z, xAxis, yAxis); 

ax = mplt.subplot(111)
testLine = []; lerpInput = start; lerpInterval = 64
for _ in range(numSteps * lerpInterval):
    testLine.append(lerpGradient(lerpInput, xAxis, step, gX[0]))
    lerpInput += step/float(lerpInterval)

for i in range(len(gX[0])):
    ax.axhline(gX[0][i], alpha = 0.3, color='g', label='gradient point ' + str(i))
ax.plot(testLine, label='gradient lerped on a 1/64th sub-interval'); 
ax.legend(); mplt.show()