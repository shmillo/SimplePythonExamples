import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as mplt

fig, ax = mplt.subplots(1,1); ax.set_xlim([-2, 2]); ax.set_ylim([-2, 2])
line, = mplt.plot([], [], 'r.', markersize=10, alpha=1,animated=True)

def animation_func(i):
  global X, Y, angleOfRotation
  
  angleOfRotation = (angleOfRotation + 1) 
  cosScalar = np.cos(angleOfRotation); sinScalar = np.sin(angleOfRotation)

  xdat = np.empty_like(X); ydat =  np.empty_like(Y)
  xdat[2:4, 2:4] = ((cosScalar * X[2:4, 2:4]) - (sinScalar * Y[2:4, 2:4]))
  ydat[2:4, 2:4] = ((sinScalar * X[2:4, 2:4]) + (cosScalar * Y[2:4, 2:4]))
  
  cosScalar = np.cos(angleOfRotation * 2.0); sinScalar = np.sin(angleOfRotation * 2.0)
  xdat[5:7, 5:7] = ((cosScalar * X[5:7, 5:7] ) - (sinScalar * Y[5:7, 5:7] ))
  ydat[5:7, 5:7] = ((sinScalar * X[5:7, 5:7] ) + (cosScalar * Y[5:7, 5:7] ))
  
  line.set_data(xdat, ydat)
  return line
  
angleOfRotation = 0; 
xAxis = np.arange(-2.0, 2.0, 0.5); yAxis = np.arange(-2.0, 2.0, 0.5); 
X,Y = np.meshgrid(xAxis,yAxis); #print(X)

animation = FuncAnimation(fig, func=animation_func, frames=np.linspace(0, 360), interval=200)
animation.save('rotate_2_Squares.gif')
mplt.show()