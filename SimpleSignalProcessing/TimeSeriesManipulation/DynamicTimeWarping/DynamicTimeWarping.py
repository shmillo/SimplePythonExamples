import numpy as np
import matplotlib.pyplot as mplt

def lerp(start, stop, t):
    return ((1.0 - t) * start) + (t * stop)

def dtw(s, t, window):
    n, m = len(s), len(t)
    w = np.max([window, abs(n-m)])
    dtwMatrix = np.zeros((n+1, m+1))
    
    for i in range(n+1):
        for j in range(m+1):
            dtwMatrix[i, j] = np.inf
    dtwMatrix[0, 0] = 0
    
    for i in range(1, n+1):
        for j in range(np.max([1, i-w]), np.min([m, i+w])+1):
            dtwMatrix[i, j] = 0
    
    for i in range(1, n+1):
        for j in range(np.max([1, i-w]), np.min([m, i+w])+1):
            cost = abs(s[i-1] - t[j-1])

            lastMin = np.min([dtwMatrix[i-1, j], dtwMatrix[i, j-1], dtwMatrix[i-1, j-1]])
            dtwMatrix[i, j] = cost + lastMin
    return dtwMatrix

fig, (ax1, ax2, ax3, ax4) = mplt.subplots(4, figsize=(8,8))

seriesOriginal = np.random.random([20, 1])
seriesModified = seriesOriginal * np.random.random([20, 1])

lengths = dtw(seriesOriginal, seriesModified, window=0); print(lengths.shape[0])

indices = []; distances = []; startPoints = []
for i in range(lengths.shape[0] - 1):
    indices.append(lengths[i].argmin())
    distances.append(lengths[i][indices[i]])
    point = seriesOriginal[indices[i]]
    startPoints.append(point)
indices = np.array(indices); distances = np.array(distances); startPoints = np.array(startPoints)
#print(indices, distances, startPoints)

interpolationStep = 0.1; interpolationAxis = np.arange(0.0, 1.0 + interpolationStep, interpolationStep)

interpolatedPointArray = np.zeros([startPoints.shape[0], interpolationAxis.shape[0]])
for i in range(startPoints.shape[0]):
    interpolatedPointArray[i] = lerp(startPoints[i], seriesModified[i], interpolationAxis)
    plotAxis = np.ones(interpolatedPointArray.shape[1]) * i
    if(i == startPoints.shape[0] - 1):
        ax3.plot(plotAxis, interpolatedPointArray[i], linewidth=0.5, color='k', label='interpolated distances')
    else:
        ax3.plot(plotAxis, interpolatedPointArray[i], linewidth=0.5, color='k')
ax3.plot(seriesOriginal, label='first time series'); ax3.plot(seriesModified, label='second time series')
ax3.legend(loc='lower left')

for i in range(interpolatedPointArray.shape[1]):
    line = []
    for j in range(interpolatedPointArray.shape[0]):
        line.append(interpolatedPointArray[j][i])
    if(i == interpolatedPointArray.shape[1] - 1):
        ax4.plot(line, linewidth=0.5, color='k', label='horizontally interpolated points')
    else:
        ax4.plot(line, linewidth=0.5, color='k')
ax4.legend(loc='upper right')

ax1.plot(seriesOriginal, label='first time series'); ax1.legend()
ax2.plot(seriesModified, label='second time series'); ax2.legend()
mplt.show()