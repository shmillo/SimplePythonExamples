import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

def computeState(nCell, eCell, sCell, wCell):
  
  sum = (nCell + eCell + sCell + wCell)%2 
  
  state = 0
  if(sum == 0): 
    state = 0
  elif(sum == 1): 
    state = 1
  
  return state

def animFunc(i):
  global X, Y, nx, ny, valueArray
  
  ax.clear(); ax.set_xlim([0, nx]); ax.set_ylim([0, ny])
  ax.scatter(X, Y, c=valueArray)
  
  tempMatrix = np.copy(valueArray)
  for i in range(1, nx-1):
    for j in range(1, ny-1):
      
      nCell = valueArray[i][j+1]
      eCell = valueArray[i + 1][j]
      sCell = valueArray[i][j - 1]
      wCell = valueArray[i - 1][j]
      tempMatrix[i][j] = computeState(nCell, eCell, sCell, wCell)
  valueArray = np.copy(tempMatrix)
  
nx = 50; ny = 50
xAxis = np.linspace(0, nx, num=nx); yAxis = np.linspace(0, ny, num=ny); X, Y = np.meshgrid(xAxis, yAxis)

valueArray = np.zeros([nx, ny])
for i in range(10, nx - 10, 2):
  for j in range(10, ny - 10, 2):
    valueArray[i][j] = np.random.choice([0, 1])

fig, ax = mplt.subplots(1); ax.set_xlim([0, nx]); ax.set_ylim([0, ny])
anim = FuncAnimation(fig, func=animFunc, frames=range(100), interval=100)
anim.save('fAnim.gif')
mplt.show()
