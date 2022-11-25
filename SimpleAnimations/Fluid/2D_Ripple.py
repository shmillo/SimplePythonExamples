import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

def animFunction(i):
    global cols, rows, current, previous, dampingFactor, xAxis, yAxis, totalNumFrames

    locationX = int(cols * 0.5); locationY = int(rows * 0.5); points = 4; amount = 10500 * np.exp(-50.0 * (i/totalNumFrames))
    for i in range(points):
        for j in range(points):
            previous[locationX + (i)][locationY + (j)] = amount

    for i in range(1, cols - 1):
        for j in range(1, rows - 1):
            tempValue = (previous[i-1][j] + previous[i+1][j] + previous[i][j-1] + previous[i][j+1])/2.0
            current[i][j] = tempValue - (1.1 * current[i][j])
            current[i][j] *= dampingFactor
    
    mplt.contourf(xAxis, yAxis, current, cmap='ocean')
    temp = previous; previous = current; current = temp

fig, ax = mplt.subplots(1,1)

cols = 50; rows = 50; totalNumFrames = 500; dampingFactor = 0.999919
current = np.zeros([cols, rows]); previous = np.zeros([cols, rows])
xAxis = np.linspace(0.36, 0.38, num=cols); yAxis = np.linspace(0.36, 0.38, num=rows)

anim = FuncAnimation(fig, func=animFunction, frames=np.linspace(0, totalNumFrames, num=totalNumFrames), interval=1)
anim.save('2D_Ripple_T1.gif')
#mplt.show()