import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

def laplacian(data, x, y):
    global grid, weights
  
    laplaceSum = 0.0
    laplaceSum += weights[0] * grid[x][y][data]
    laplaceSum += weights[1] * grid[x-1][y][data]
    laplaceSum += weights[2] * grid[x+1][y][data]
    laplaceSum += weights[3] * grid[x][y+1][data]
    laplaceSum += weights[4] * grid[x][y-1][data]
    laplaceSum += weights[5] * grid[x-1][y-1][data]
    laplaceSum += weights[6] * grid[x+1][y-1][data]
    laplaceSum += weights[7] * grid[x+1][y+1][data]
    laplaceSum += weights[8] * grid[x-1][y+1][data]

    return laplaceSum

def calculateReactionDiffusion():
    global grid, nextArr, gridHeight, gridWidth, dA, dB, feed, kF

    nextArr = grid.copy()

    #update reaction
    for j in range(1, gridWidth - 1):
        for k in range(1, gridHeight - 1):
            
            a = grid[j][k][0]; b = grid[j][k][1]
            
            nextArr[j][k][0] = a + (dA * laplacian(0, j, k)) - (a*b*b) + (feed * (1.0 - a))
            nextArr[j][k][1] = b + (dB * laplacian(1, j, k)) + (a*b*b) - ((kF + feed) * b)
            
            if(nextArr[j][k][0] > 1.0):
                nextArr[j][k][0] = 1.0
            elif(nextArr[j][k][0] < 0.0):
                nextArr[j][k][0] = 0.0 
            
            if(nextArr[j][k][1] > 1.0):
                nextArr[j][k][1] = 1.0
            elif(nextArr[j][k][1] < 0.0):
                nextArr[j][k][1] = 0.0 

    ax.clear(); ax.set_xlim([0, gridWidth]); ax.set_ylim([0, gridHeight]); ax.set_facecolor('black')
    ax.scatter(X, Y, c=(grid[:, :, 0] - grid[:, :, 1]), cmap='winter_r')
    
    grid = nextArr.copy()

def animFunc(i):
    global grid, xAxis, yAxis, X, Y

    calculateReactionDiffusion()
 

gridWidth = 50; gridHeight = 50; grid = np.zeros([gridWidth, gridHeight, 2], dtype=np.float32); nextArr = np.zeros_like(grid)
grid[:, :, 0] = 1.0; nextArr[:, :, 0] = 1.0

xAxis = np.arange(0, gridWidth, 1); yAxis = np.arange(0, gridHeight, 1); X, Y = np.meshgrid(xAxis, yAxis)

#add sources
for j in range(24, 26):
    for k in range(24, 26):
        grid[j][k][1] = 1.0

fig, ax = mplt.subplots(1); fig.tight_layout(pad=0); fig.set_facecolor('black')
ax.set_xlim([0, gridWidth]); ax.set_ylim([0, gridHeight]); ax.set_facecolor('black')

weights = np.ones([9,1]); weights[0] = -1.0;  weights[1] = 0.2; weights[2] = 0.2; weights[3] = 0.2; weights[4] = 0.2; 
weights[5] = 0.05; weights[6] = 0.05; weights[7] = 0.05; weights[8] = 0.05; 

color = np.zeros([gridWidth, gridHeight, 4], dtype=np.float32); color[:][:][3] = 1.0

dA = 1.0; dB = 0.5; feed = 0.055; kF = 0.062

anim = FuncAnimation(fig, func=animFunc, frames=range(100), interval=1)
#anim.save("reactionDiffusion.gif", fps=30)
mplt.show()