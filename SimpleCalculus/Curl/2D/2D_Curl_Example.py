import numpy as np
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as mplt

def funcX(x, y): return np.cos(x) + np.sin(y)
def funcY(x, y): return np.cos(x*y)

firstBound = -10.0; secondBound = 10.0; step = 0.1
xAxis = np.arange(firstBound, secondBound, step)
yAxis = np.arange(firstBound, secondBound, step)

X,Y = np.meshgrid(xAxis, yAxis); Fx = funcX(X,Y); Fy = funcY(X,Y);

dXFx, dYFx = np.gradient(Fx); dXFy, dYFy = np.gradient(Fy)

curl = dXFy - dYFx; 

fig = mplt.figure(figsize = (12,12))
ax = fig.add_subplot(111, projection='3d')
ax.scatter3D(X,Y,curl,cmap='hot',c=curl) 
ax.azim = 90
ax.dist = 5
ax.elev = 90
#ax.plot_surface(X,Y,Fy)
#mplt.contourf(X,Y,curl)
#mplt.contour(X,Y,curl)
#mplt.streamplot(X,Y,Fx,Fy)
mplt.show()