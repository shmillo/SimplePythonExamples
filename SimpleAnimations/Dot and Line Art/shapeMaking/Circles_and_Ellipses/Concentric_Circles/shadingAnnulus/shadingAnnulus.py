import numpy as np
import matplotlib.pyplot as mplt

resolution = 2000; l = 1000; w = 1000; gridL = 1 + (l * 2); gridW = 1 + (w * 2); hashGrid = np.zeros([gridL, gridW, 4], dtype=np.float32)
grid = np.linspace(0, gridL, gridL).astype(np.int32)

xAngle = np.linspace(0, 360, num=resolution, endpoint=False); xAngle *= np.pi/180.0; yAngle = np.copy(xAngle)
xAngle = np.cos(xAngle); yAngle = np.sin(yAngle); 

radii = [1.0, 5.0]
for i in range(len(radii)):

    radius = l/radii[i]
    xAngleTemp = np.round(xAngle * radius).astype(np.int32)
    yAngleTemp = np.round(yAngle * radius).astype(np.int32)
    hashGrid[xAngleTemp + l, yAngleTemp + w, :] = 1.0

radiusOuter = l/radii[0]; radiusInner = l/radii[1]

shadeIdx = grid[grid**2 < radiusOuter**2]; shadeIdx = shadeIdx[shadeIdx**2 > radiusInner**2]
shadeIdxX = (np.matmul(np.reshape(xAngle, [xAngle.shape[0], 1]), np.reshape(shadeIdx, [1, shadeIdx.shape[0]])) + l).astype(np.int32)
shadeIdxY = (np.matmul(np.reshape(yAngle, [yAngle.shape[0], 1]), np.reshape(shadeIdx, [1, shadeIdx.shape[0]])) + w).astype(np.int32)
hashGrid[shadeIdxX.flatten(), shadeIdxY.flatten()] = [1.0, 1.0, 1.0, 1.0]

mplt.imshow(hashGrid)
mplt.show()
