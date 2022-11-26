import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.collections import PolyCollection

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


fig = mplt.figure(); ax = fig.add_subplot(111, projection='3d')
fig.set_size_inches(3.5, 3.5); fig.tight_layout(pad=0); ax.axis('off')

perm = np.arange(256); np.random.shuffle(perm) #print(perm)
GradientSizeTable = 256; gradients = [0.0] * (GradientSizeTable * 3)

Init()

timeSteps = 10; numSteps = 100; destinationValue = 5.0; noiseIndex = 0.0; noiseIncrement = 1.0/float(numSteps); offset = 0.5
xAxis = np.linspace(0, destinationValue, num=numSteps); yAxis = np.linspace(0, destinationValue, num=numSteps); zAxis = np.linspace(0, timeSteps, num=int(numSteps**2.0))
noiseArray = [ [0.0] * numSteps for _ in range(numSteps) ]; alphaArray = [ [0.0] * numSteps for _ in range(numSteps) ]
X, Y = np.meshgrid(xAxis, yAxis)


for j in range(numSteps):
    for k in range(numSteps):
        value = (Noise(xAxis[j], yAxis[k], 0) + offset)
        noiseArray[j][k] = 500.0 * expander(value, 0.65, 0.51)
        alphaArray[j][k] = constrain(expander(value, 0.65, 0.51), 0.1, 1.0)

nA = np.array(noiseArray) 
#ax.plot_surface(X, Y, nA)
#ax.plot_wireframe(X, Y, nA, rstride=10, cstride=10)
#ax.plot_surface(X, Y, nA, rstride=1, cstride=1, color='b', shade=False, lw=.5)
ax.scatter(X, Y, zAxis, s=noiseArray, c=noiseArray, cmap='Blues', alpha=alphaArray) 
mplt.show()