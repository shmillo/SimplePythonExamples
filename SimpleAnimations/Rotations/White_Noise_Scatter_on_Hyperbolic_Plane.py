import matplotlib.pyplot as mplt
import numpy as np
from matplotlib.animation import FuncAnimation
def funcX(x, y): return np.cos(x) + np.sin(x*y)
def funcY(x, y): return np.cos(x*y)

def animFunc(i):
  global Zx, Zy

  ax.clear()
  ax.axis('off'); ax.axis('square'); ax.dist = 20; ax.set_xlim([-1.01,1.01]); ax.set_ylim([-1.01, 1.01])
  ax.scatter(Zx, Zy, s=10.0*np.random.random(Zx.shape), alpha=np.random.random(Zx.shape), cmap='Blues')


fig, ax = mplt.subplots(1, dpi=200); ax.axis('off'); ax.axis('square'); ax.dist = 20; ax.set_xlim([-1.01,1.01]); ax.set_ylim([-1.01, 1.01])

numSteps = 50
xAxis = np.linspace(-1.0, 1.0, num=numSteps); yAxis = np.linspace(-1.0, 1.0, num=numSteps); X,Y = np.meshgrid(xAxis, yAxis)

Zx = X*(1.0 - (Y**2.0)*0.5)**0.5; Zy = Y*(1.0 - (X**2.0)*0.5)**0.5

aFunc = FuncAnimation(fig, func=animFunc, frames=np.linspace(0, 50, num=50), interval=1); aFunc.save('globe.gif')
aFunc.save('globe_higher_dpi.gif')
mplt.show()