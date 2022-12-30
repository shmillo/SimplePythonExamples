import numpy as np
import math
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

def animFunc(i):
    global a, b, v, dt, dx, u, U

    v = np.copy(u)
    for rk in range(5, 1, -1):
        dvdx = (v[idc] - v[idl])/dx
        dvdx2 = (v[idl] - 2.0*v[idc] + v[idr])/(dx**2.0)
        v = u + (dt/rk) * (-U*dvdx + nu*dvdx2)
    u = np.copy(v)

    ax.clear()
    ax.set_xlim([a, b]); ax.set_ylim([0.0, 1.0])
    ax.plot(x, u, color='k')

N = 500
a = -1.0; b = 1.0
x = np.linspace(a, (b - (b - a)/N), num=N); dx = x[1] - x[0]

u = np.cos(np.pi * x); u = np.exp(-30.0 * x**2.0)
U = 2.0; nu = 0.1
dt = 1.0/((2.0*U/dx) + 4.0*nu/(dx**2.0)); dt *= 3.2

startTime = 0.0; finalTime = 10.0
nSteps = math.ceil(finalTime/dt); dt = finalTime/nSteps

idc = []; idl = []; idr = []
for i in range(N):
    idc.append( i )
    idl.append( ((N - 1) + i)%N )
    idr.append( (2 + i)%N )
idc = np.array(idc); idl = np.array(idl); idr = np.array(idr)

fig, ax = mplt.subplots(1)
anim = FuncAnimation(fig, func=animFunc, frames=range(nSteps), interval=1)
#anim.save('advectionGif.gif', fps=30)
mplt.show()