import numpy as np
import matplotlib.pyplot as mplt

def f(x, y):
    return 2.0*x + 3.0*y

def bilinearInterpolation(x, y, lX, lY):
    
    fq11 = f(x[0], y[0]); fq12 = f(x[0], y[1])
    fq21 = f(x[1], y[0]); fq22 = f(x[1], y[1])
    
    tempOne = (1.0/((x[1] - x[0])*(y[1] - y[0]))) 
    tempTwo = x[1] - lX; tempThree = lX - x[0]
    tempFour = y[1] - lY; tempFive = lY - y[0]

    outVal = fq11 * tempTwo * tempFour
    outVal += fq21 * tempThree * tempFour
    outVal += fq12 * tempTwo * tempFive
    outVal += fq22 * tempThree * tempFive
    
    return outVal * tempOne

x1 = 0.0; x2 = 1.0
y1 = 1.0; y2 = 2.0
xData = [x1, x2]; yData = [y1, y2]; X, Y = np.meshgrid(xData, yData); fData = f(X, Y)

numSteps = 100; step = 1.0/numSteps; lX = 0.0
interpXData = np.zeros([numSteps, numSteps]); interpYData = np.zeros([numSteps, numSteps]); interpFData = np.zeros([numSteps, numSteps])
for i in range(numSteps):
    lY = 0.0
    for j in range(numSteps):
        currentX = xData[0] + lX; currentY = yData[0] + lY
        outVal = bilinearInterpolation(xData, yData, currentX, currentY)
        interpXData[i][j] = currentX; interpYData[i][j] = currentY; interpFData[i][j] = outVal
        lY += step
    lX += step
print(fData)
print(interpFData[0][0], interpFData[numSteps - 1][0])
print(interpFData[0][numSteps - 1], interpFData[numSteps - 1][numSteps - 1])

fig, (ax1, ax2) = mplt.subplots(2)
ax1.contourf(X, Y, fData); ax1.set_label('exact values')
ax1.set_title(label='actual values', fontfamily='serif', loc='right', fontsize='medium')

ax2.contourf(interpXData, interpYData, interpFData)
ax2.set_title(label='inteprolated values', fontfamily='serif', loc='right', fontsize='medium')

fig = mplt.figure()
ax3 = fig.add_subplot(111, projection='3d')
ax3.plot_surface(interpXData, interpYData, interpFData)
ax3.set_title(label='3D Visualization', fontfamily='serif', loc='right', fontsize='medium')

mplt.show()



