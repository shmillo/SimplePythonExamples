import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

class Grain:
    def __init__(self, N_points, amplitude, delta=0.05):
        self.N_points = N_points
        self.points = np.random.uniform(-1, 1, size=(2,self.N_points))
        self.amplitude = amplitude
        self.delta = delta
    def move(self, **amplitude_params):
        angles = np.random.uniform(0, 2*np.pi, size=self.N_points)
        dr = self.delta * np.array([np.cos(angles), np.sin(angles)]) \
              * self.amplitude(*self.points, **amplitude_params) / 2
        self.prev_points = np.copy(self.points)
        self.points += dr

def amplitude(xv, yv, n, m): 
    return np.abs(np.sin(n*np.pi*xv/2)*np.sin(m*np.pi*yv/2) - np.sin(m*np.pi*xv/2)*np.sin(n*np.pi*yv/2))

x = y = np.linspace(-1, 1, 1000)
xv, yv = np.meshgrid(x, y)

ensemble = Grain(10000, amplitude, delta=0.05)

fig, ax = mplt.subplots(1,1, figsize=(10,10)); fig.tight_layout(pad=0)
ln1, = mplt.plot([], [], 'o', ms=2, color='white')
ax.set_xlim(-1,1); ax.set_ylim(-1,1)
ax.set_facecolor('black')
ax.axes.get_xaxis().set_visible(False)
ax.axes.get_yaxis().set_visible(False)

def animate(i):
    if i%5==0:
        if(i <= 250):
            ensemble.move(n=3, m=5)
        elif(i > 250 and i <= 500):
            ensemble.move(n=7, m=3)
        elif(i > 500):
            ensemble.move(n=1, m=7)

    points = ensemble.prev_points + (i%5)/5 *(ensemble.points-ensemble.prev_points)
    ln1.set_data(*points)

ani = FuncAnimation(fig, animate, frames=range(500), interval=50)
ani.save("eigenModeAnimation2.gif", fps=30)
