import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

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

def f(x, m, b):
    return m*x + b

def plotGridWithHeight():
    global h, w, noiseArr

    nR = w + 1; numUp = w
    for j in range(numUp + 1):
        xCoords = []; yCoords = []; uZCoords = []; lZCoords = []
        for x in range(nR - j):
            y = int(f(x, 1, j))
            xCoords.append(x); yCoords.append(y); 
            uZCoords.append(noiseArr[x][y]); lZCoords.append(noiseArr[y][x]) 
        if(j != 0):
            ax.plot(yCoords, xCoords, lZCoords, color=colorString)
        ax.plot(xCoords, yCoords, uZCoords, color=colorString)

    for x in range(w + 1):
        xCoords = []; yCoords = []; uZCoords = []; lZCoords = []
        for y in range(h + 1):
            xCoords.append(x); yCoords.append(y)
            uZCoords.append(noiseArr[x][y]); lZCoords.append(noiseArr[y][x])
        ax.plot(xCoords, yCoords, uZCoords, color=colorString)
        ax.plot(yCoords, xCoords, lZCoords, color=colorString)

def animFunc(i):
    global w, h, noiseArr, xR, yR, zR, globalNoiseInc, localNoiseInc
    
    ax.clear(); ax.axis('off'); ax.set_facecolor('black'); ax.dist = 6; ax.azim = -90; ax.elev = 60
    ax.set_xlim([0.0, w+1]); ax.set_ylim([0.0, h+1]); ax.set_zlim([0.0, 1.0])
    
    yR = globalNoiseInc
    for j in range(w + 1):
        xR = 0.0
        for k in range(h + 1):
            noiseArr[k][j] = Noise(xR, yR, 0.0)
            xR += localNoiseInc
        yR += localNoiseInc
    globalNoiseInc += 0.01

    plotGridWithHeight()


w = 50; h = 50 

fig = mplt.figure(figsize=(8, 8)); fig.set_facecolor('black'); fig.tight_layout(pad=0)
ax = fig.add_subplot(111, projection='3d'); colorString = 'g'
ax.axis('off'); ax.set_facecolor('black'); ax.dist = 6; ax.azim = -90; ax.elev = 90
ax.set_xlim([0.0, w+1]); ax.set_ylim([0.0, h+1]); ax.set_zlim([0.0, 1.0])

perm = np.arange(256); np.random.shuffle(perm) #print(perm)
GradientSizeTable = 256; gradients = [0.0] * (GradientSizeTable * 3)
Init()

noiseArr = np.zeros([w+1,h+1]); xR, yR, zR = 0.0, 0.0, 0.0; localNoiseInc = 0.1; globalNoiseInc = 0.0

anim = FuncAnimation(fig, func=animFunc, frames=range(500), interval=1)
anim.save('terrainScroller.gif', fps=60)
mplt.show()
