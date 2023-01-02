from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as mplt
import numpy as np

def animFunc(i):
  global  nx, ny, positionArray, velocitiesArray, X, Y, xAxis, yAxis, dXMax, dYMax, dt
  
  ax.clear(); ax.set_xlim([-nx, nx]); ax.set_ylim([-ny, ny]); ax.axis('off'); 
  ax.scatter(positionArray[0], positionArray[1], s = 0.01, c = np.sqrt(positionArray[0]**2.0 + positionArray[1]**2.0), cmap='prism')
  
  positionArray = positionArray + velocitiesArray
  for i in range(nParticles):
    for j in range(nParticles):
      velocitiesArray[0][i][j] = np.random.choice([-1.0, 1.0]) * np.random.rand() * (dXMax/dt)
      velocitiesArray[1][i][j] = np.random.choice([-1.0, 1.0]) * np.random.rand() * (dYMax/dt)

nx = 50; ny = 50; dXMax = 0.50; dYMax = 0.50; dt = 1.0/10.0; nParticles = 100
xAxis = np.linspace(0, 50, num=nParticles); yAxis = np.linspace(0, 50, num=nParticles); X, Y = np.meshgrid(xAxis, yAxis)

positionArray = np.zeros([2, nParticles, nParticles])
velocitiesArray = np.zeros([2, nParticles, nParticles])
for i in range(nParticles):
  for j in range(nParticles):
    velocitiesArray[0][i][j] = np.random.choice([-1.0, 1.0]) * np.random.rand() * (dXMax/dt)
    velocitiesArray[1][i][j] = np.random.choice([-1.0, 1.0]) * np.random.rand() * (dYMax/dt)

fig, (ax) = mplt.subplots(1);  fig.tight_layout(pad=0); 
ax.axis('off'); ax.set_xlim([-nx, nx]); ax.set_ylim([-ny, ny])

anim = FuncAnimation(fig, func=animFunc, frames=range(100), interval=1)
anim.save('randomWalk.gif')
mplt.show()
  