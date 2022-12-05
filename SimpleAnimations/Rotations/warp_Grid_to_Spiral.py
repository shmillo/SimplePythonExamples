import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation
import numpy as np

def funcAnim(i):
    global X, Y, hX, hY, rX, rY, lerp, sizeArr, cosScalar, sinScalar, angleOfRotation, rate

    outputX = ((1.0 - lerp) * X) + (lerp * rX); outputY = ((1.0 - lerp) * Y) + (lerp * rY)
    lerp += 0.005
    if(lerp >= 1.0):
        lerp = 1.0
    
    outputX *= 1.0 + (lerp * 0.01); outputY *= 1.0 + (lerp * 0.01)

    if(angleOfRotation.max() <= 1.0):
        ax.elev = 90 * lerp
        angleOfRotation = angleOfRotation + rate 
        cosScalar = np.cos(angleOfRotation); sinScalar = np.sin(angleOfRotation)
    else:
        rate = np.ones_like(X) * 0.006
        angleOfRotation = angleOfRotation + rate 
        cosScalar = np.cos(angleOfRotation); sinScalar = np.sin(angleOfRotation)

    outX = (cosScalar * outputX) - (sinScalar * outputY); outY = (sinScalar * outputX) + (cosScalar * outputY)

    ax.clear(); ax.axis('off'); ax.set_xlim([-1.0, 1.0]); ax.set_ylim([-1.0, 1.0])
    ax.scatter(outX, outY, s=sizeArr, color='k')

fig, ax = mplt.subplots(1, dpi=300); fig.tight_layout(pad=0); ax.axis('off')
ax.set_xlim([-1.0, 1.0]); ax.set_ylim([-1.0, 1.0])

step = 0.1; lerp = 0.0; cosScalar = 0.0; sinScalar = 0.0
xAxis = np.arange(-1.0, 1.0, step); yAxis = np.arange(-1.0, 1.0, step); X,Y = np.meshgrid(xAxis, yAxis)

angleOfRotation = np.zeros_like(X); rate = np.zeros_like(X); rateInc = 0.09
for i in range(rate.shape[0]):
    for y in range(rate.shape[1]):
        rate[i][y] = rateInc
        rate[y][i] = rateInc
        rate[rate.shape[0] - 1 - i][rate.shape[1] - 1 - y] = rateInc
        rate[rate.shape[1] - 1 - y][rate.shape[0] - 1 - i] = rateInc
    rateInc *= 0.8
sizeArr = np.ones_like(rate) - rate

hX = X*(1.0 - (Y**2.0 * 0.5))**0.5; hY = Y*(1.0 - (X**2.0 * 0.5))**0.5
rsq = X**2.0 + Y**2.0 + np.ones_like(X); rX = X * rsq; rY = Y * rsq

animF = FuncAnimation(fig, func=funcAnim, frames=np.linspace(0, 200, num=200), interval=1)
animF.save('grid_Morph_Hyperbolic_Pincushion_With_Skewed_Spin_Rate_lo_DPI.gif')
mplt.show()