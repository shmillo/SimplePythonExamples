import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as mplt

fig, ax = mplt.subplots(1,1); ax.set_xlim([-2, 2]); ax.set_ylim([-2, 2])
line, = mplt.plot([], [], 'r.', markersize=3.0, alpha=1, animated=True)

def animation_func(i):
  global X, Y, angleOfRotation

  angleOfRotation = angleOfRotation + 1 
  cosScalar = np.cos(angleOfRotation); sinScalar = np.sin(angleOfRotation)

  xdat = (cosScalar * X) - (sinScalar * Y); ydat = (sinScalar * X) + (cosScalar * Y)
  line.set_data(xdat, ydat)

  return line
  
angleOfRotation = 0
xAxis = np.arange(-2.0, 2.0, 0.5); yAxis = np.arange(-2.0, 2.0, 0.5)
X, Y = np.meshgrid(xAxis, yAxis)

animation = FuncAnimation(fig, func=animation_func, frames=np.linspace(0, 360), interval=200)
animation.save('spinningGrid.gif')
mplt.show()