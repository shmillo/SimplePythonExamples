import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation
import numpy as np

def Init():
    global gradients, GradientSizeTable

    for i in range(GradientSizeTable):
        z = 1.0 - 2.0 * np.random.rand()
        r = (1.0 - z**2.0)**0.5
        theta = 2.0 * np.pi * np.random.rand()
        index = i * 3
        gradients[index] = r * np.cos(theta)
        gradients[index + 1] = r * np.sin(theta)
        gradients[index + 2] = z

def Smooth(x):
    return x**2.0 * (3 - 2*x)

def lerp(t, v0, v1):
    return v0 + t*(v1 - v0)

def Permutate(x):
    global GradientSizeTable, perm
    mask = GradientSizeTable - 1; return perm[(x&mask)]

def Index(ix, iy, iz):
    return Permutate(ix + Permutate(iy + Permutate(iz)))

def Lattice(ix, iy, iz, fx, fy, fz):
    global gradients
    idx = Index(ix, iy, iz); g = idx * 3
    return (gradients[g]*fx) + (gradients[g+1]*fy) + (gradients[g+2]*fz)

def Noise(x,y,z):
    ix = int(x); fx0 = x - ix; fx1 = fx0 - 1; wx = Smooth(fx0)
    iy = int(y); fy0 = y - iy; fy1 = fy0 - 1; wy = Smooth(fy0)
    iz = int(z); fz0 = z - iz; fz1 = fz0 - 1; wz = Smooth(fz0)

    vx0 = Lattice(ix, iy, iz, fx0, fy0, fz0); vx1 = Lattice(ix + 1, iy, iz, fx1, fy0, fz0)
    vy0 = lerp(wx, vx0, vx1)

    vx0 = Lattice(ix, iy + 1, iz, fx0, fy1, fz0); vx1 = Lattice(ix + 1, iy + 1, iz, fx1, fy1, fz0)
    vy1 = lerp(wx, vx0, vx1)

    vz0 = lerp(wy, vy0, vy1)

    vx0 = Lattice(ix, iy, iz + 1, fx0, fy0, fz1); vx1 = Lattice(ix + 1, iy, iz + 1, fx0, fy1, fz1)
    vy0 = lerp(wx, vx0, vx1)

    vx0 = Lattice(ix, iy + 1, iz + 1, fx0, fy1, fz1); vx1 = Lattice(ix + 1, iy + 1, iz + 1, fx1, fy1, fz1)
    vy1 = lerp(wx, vx0, vx1)

    vz1 = lerp(wy, vy0, vy1)

    return lerp(wz, vz0, vz1)

def constrain(v, b1, b2):
    rv = 0.0
    if(v < b1):
        rv = b1
    elif(v > b2):
        rv = b2
    else:
        rv = v
    return rv

def expander(x, t, r):
    return ((x - t)/r) + t

def animFunc(i):
    global noiseArrayX, noiseArrayY, X, Y, noiseInc

    noiseInc += 1.0/40.0
    for q in range(numSteps):
        for y in range(numSteps):
            noiseArrayX[q][y] = (Noise(xAxis[q]+noiseInc, yAxis[y], noiseInc))
    noiseArrayX = noiseArrayX / np.linalg.norm(noiseArrayX) 

    Zx = noiseArrayX*(1.0 - (noiseArrayY**2.0)*0.5)**0.5; 
    xA = X*(1.0 - (Y**2.0)*0.5)**0.5; yA = Y*(1.0 - (X**2.0)*0.5)**0.5

    ax.clear(); mplt.axis('off'); ax.set_xlim([-1.1, 1.1]); ax.set_ylim([-1.1, 1.1]); ax.dist=20; ax.axis('square')
    ax.scatter(xA, yA, s=10.0*Zx, cmap='blues') 

fig, ax = mplt.subplots(1,1, dpi=150); mplt.axis('off'); ax.set_xlim([-1.1, 1.1]); ax.set_ylim([-1.1, 1.1]); ax.dist=20

perm = np.arange(256); np.random.shuffle(perm); GradientSizeTable = 256; gradients = [0.0] * (GradientSizeTable * 3)

Init()

numSteps = 50; offset = 0.31; noiseInc = 0.0
xAxis = np.linspace(-1.0, 1.0, num=numSteps); yAxis = np.linspace(-1.0, 1.0, num=numSteps); X,Y = np.meshgrid(xAxis, yAxis)
noiseArrayX = np.zeros_like(X); noiseArrayY = np.zeros_like(X)

animF = FuncAnimation(fig, func=animFunc, frames=np.linspace(0, 100, num=100), interval=1)
animF.save('pNoise_Globe.gif')
mplt.show()