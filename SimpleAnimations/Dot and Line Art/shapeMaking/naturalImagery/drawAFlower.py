import numpy as np
import matplotlib.pyplot as mplt
from mpl_toolkits.mplot3d import Axes3D

petalsPerRevolution = 6.6
radiusResolution = 30
petalResolution = 10
numberOfPetals = 140
petalTilt = -1.2
openness = [0.11, 1.1] 

tempVarOne = numberOfPetals * ((2.0 * np.pi)/petalsPerRevolution)
tempVarTwo = int(numberOfPetals * petalResolution + 1)
theta = np.reshape(np.linspace(0, tempVarOne, tempVarTwo), [1, tempVarTwo]); #print(theta.shape)
[R, Theta] = np.meshgrid(np.linspace(0, 1, radiusResolution), theta, indexing='xy')
R = R.T; Theta = Theta.T; #print(Theta.shape)
x = 1.0 - np.abs(1.0 - (np.mod(petalsPerRevolution*Theta, 2.0*np.pi)/np.pi))**2.0 * 0.7
phi = np.pi * 0.5 * np.linspace(openness[0], openness[1], tempVarTwo)**2.0
y = petalTilt * (R**2.0) * (1.27689 * R - 1.0)**2.0 * np.sin(phi)
R2 = x * (R * np.sin(phi) + y * np.cos(phi))

X = R2 * np.sin(Theta)
Y = R2 * np.cos(Theta)
Z = x * (R*np.cos(phi) - y*np.sin(phi))
C = np.hypot(np.hypot(X, Y), Z)

fig = mplt.figure(figsize = (6, 6)); ax = fig.add_subplot(111, projection='3d'); ax.axis('off'); ax.dist = 7
surf = ax.plot_surface(X, Y, Z)

mplt.show()