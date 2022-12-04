import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation
import numpy as np

def funcAnim(i):
    global X, Y, hX, hY, rX, rY, lerp

    outputX = ((1.0 - lerp) * X) + (lerp * rX); outputY = ((1.0 - lerp) * Y) + (lerp * rY)
    lerp += 0.01
    if(lerp >= 1.0):
        lerp = 1.0
    
    outputX *= 1.0 + (lerp * 0.05); outputY *= 1.0 + (lerp * 0.05)

    ax.clear(); ax.axis('off'); ax.set_xlim([-1.0, 1.0]); ax.set_ylim([-1.0, 1.0])
    ax.scatter(outputX, outputY, color='k')

fig, ax = mplt.subplots(1, dpi=100); fig.tight_layout(pad=0); ax.axis('off')
ax.set_xlim([-1.0, 1.0]); ax.set_ylim([-1.0, 1.0])

step = 0.1; lerp = 0.0
xAxis = np.arange(-1.0, 1.0, step); yAxis = np.arange(-1.0, 1.0, step); X,Y = np.meshgrid(xAxis, yAxis)

hX = X*(1.0 - (Y**2.0 * 0.5))**0.5; hY = Y*(1.0 - (X**2.0 * 0.5))**0.5

rsq = X**2.0 + Y**2.0 + np.ones_like(X)*0.4; rX = X * rsq; rY = Y * rsq

animF = FuncAnimation(fig, func=funcAnim, frames=np.linspace(0, 100, num=100), interval=1)
animF.save('grid_Morph_Hyperbolic_Barrell.gif')
mplt.show()