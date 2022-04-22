import matplotlib.pyplot as mplt
import numpy as np

def f(x):
    return x**2.0

def oneDGradient(vals, dx):

    n = len(vals)
    grad = [0.0] * n

    #forward difference for outer bounds
    grad[0] = (vals[1] - vals[0]) / dx
    for i in range(1, n - 1):
        #central difference now that data is available
        grad[i] = (vals[i + 1] - vals[i - 1]) / (2.0 * dx)
    #forward difference for outer bounds
    grad[n - 1] = (vals[n - 1] - vals[n - 2]) / dx

    return grad

#########################################

#dimensions
Nx = 21;       # Number of X-grid points
dx = 1.0;      # x coordinate grid spacing 

########## sanity check against numpy ##

#establish X axis
X = np.arange(0, Nx, dx)
#compute function LUT
fx = X**2.0
#compute derivative in 1D
dFdX = np.gradient(fx, dx)

########## my implementation ##########

testData = [0.0] * Nx 

x = 0
for i in range(Nx):
    #function LUT
    testData[i] = f(x)
    #x axis
    x += dx

#computer gradient
gradientData = oneDGradient( testData, dx )

#########################################
 
fig, (ax1, ax2) = mplt.subplots(2)

ax1.plot(testData, label = 'my implementation')
ax1.plot(gradientData)
ax1.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

ax2.plot(fx, label = 'numpy implementation')
ax2.plot(dFdX)
ax2.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

mplt.show()

