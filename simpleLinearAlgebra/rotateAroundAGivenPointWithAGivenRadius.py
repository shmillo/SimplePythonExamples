import numpy as np
import matplotlib.pyplot as mplt

def newPointAfterRotation(x, y):
  global n, cX, cY, dx, dy
  return [cX - (y - cY), cY + (x - cX)]

dataArray = np.array([
  [0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 1, 1, 0, 0, 0],
  [0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 0, 1, 0, 0, 0, 0],
  [0, 0, 1, 1, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0]
  ], dtype = np.int8)
storageArray = np.zeros_like(dataArray)

xPoints = []; yPoints = []
n = len(dataArray); m = n - 1; 
cX = 3; cY = 3; 
radius = 3
lowerBoundX = cX - radius; upperBoundX = cX + radius + 1
lowerBoundY = cY - radius; upperBoundY = cY + radius + 1

for i in range(lowerBoundX, upperBoundX):
  for j in range(lowerBoundY, upperBoundY):
    if(i < n and j < n):
      ans = newPointAfterRotation(i, j)
      if(ans[0] < n and ans[1] < n):
        storageArray[ans[0]][ans[1]] = dataArray[i][j];
print(dataArray); print(storageArray)