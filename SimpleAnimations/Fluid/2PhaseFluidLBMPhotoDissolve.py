import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation
from PIL import Image

def grayConversion(image):
    height, width, channel = image.shape
    tempImage = np.zeros([image.shape[0], image.shape[1]], dtype=np.int64)
    for i in range(0, height):
        for j in range(0, width):
            blueComponent = image[i][j][0]
            greenComponent = image[i][j][1]
            redComponent = image[i][j][2]
            grayValue = 0.07 * blueComponent + 0.72 * greenComponent + 0.21 * redComponent
            tempImage[i][j] = grayValue 
    return tempImage

def invel(uLB, ly):
    def inner(d, x, y):
        return (1.0 - d) * uLB * (1.0 + 1.0e-4*np.sin(y/ly*2.0*np.pi))
    return inner

def macroscopic(xIn, nx, ny, v):
    rho = np.sum(fIn, axis=0)
    u = np.zeros([2, nx, ny])
    for i in range(9):
        u[0, :, :] += v[i, 0] * xIn[i, :, :]
        u[1, :, :] += v[i, 1] * xIn[i, :, :]
    u /= rho
    return rho, u

def unNormalizedMacroscopic(xIn, nx, ny, v):
    rho = np.sum(fIn, axis=0)
    u = np.zeros([2, nx, ny])
    for i in range(9):
        u[0, :, :] += v[i, 0] * xIn[i, :, :]
        u[1, :, :] += v[i, 1] * xIn[i, :, :]
    return rho, u

def equilibrium(rho, u, v, t, nx, ny):
    usqr = (3.0/2.0) * (u[0]**2.0 + u[1]**2.0)
    fEq = np.zeros([9, nx, ny])
    for i in range(9):
        cu = 3.0*((v[i, 0]*u[0, :, :]) + (v[i, 1]*u[1, :, :]))
        fEq[i, :, :] = rho * t[i] * (1.0 + cu + 0.5*cu**2.0 - usqr)
    return fEq

def macroscopic2PhaseFlow():
    global rhoOne, rhoTwo, v, nx, ny, v, omegaOne, omegaTwo, fIn, gIn, jxOne, jxTwo
    
    rhoOne = np.sum(fIn, axis=0); rhoTwo = np.sum(gIn, axis=0); jxOne.fill(0.0); jxTwo.fill(0.0)
    for i in range(9):
        jxOne[0, :, :] += v[i, 0] * fIn[i, :, :]
        jxOne[1, :, :] += v[i, 1] * fIn[i, :, :]

        jxTwo[0, :, :] += v[i, 0] * gIn[i, :, :]
        jxTwo[1, :, :] += v[i, 1] * gIn[i, :, :]

    rhoTotOmega = rhoOne*omegaOne + rhoTwo*omegaTwo
    uTotal = (jxOne*omegaOne + jxTwo*omegaTwo)/rhoTotOmega

    return rhoOne, rhoTwo, uTotal

def animFunc(x):
    global fIn, gIn, nx, ny, v, t, omegaOne, omegaTwo, gOmegaOne, gOmegaTwo

    # Macro Variables
    rhoOne, rhoTwo, uTotal = macroscopic2PhaseFlow()

    rhoOneContrib.fill(0.0); rhoTwoContrib.fill(0.0)
    for i in range(9):
        r1Temp = np.roll(np.roll((t[i] * rhoOne), v[i, 0], axis = 0), v[i, 1], axis=1)
        r2Temp = np.roll(np.roll((t[i] * rhoTwo), v[i, 0], axis = 0), v[i, 1], axis=1)
        for y in range(2):
            rhoOneContrib[y] += v[i, y] * r1Temp
            rhoTwoContrib[y] += v[i, y] * r2Temp
    uOneTotal = uTotal - gOmegaOne*rhoTwoContrib; uTwoTotal = uTotal - gOmegaTwo*rhoOneContrib

    # Collide
    feq = equilibrium(rhoOne, uOneTotal, v, t, nx, ny); gEq = equilibrium(rhoTwo, uTwoTotal, v, t, nx, ny)
    fout = fIn - omegaOne*(fIn - feq); gout = gIn - omegaTwo*(gIn - gEq)
    
    # Stream
    for i in range(9):
        fIn[i, :, :] = np.roll(np.roll(fout[i, :, :], v[i,0], axis=0), v[i,1], axis=1)
        gIn[i, :, :] = np.roll(np.roll(gout[i, :, :], v[i,0], axis=0), v[i,1], axis=1)

    mplt.imshow(rhoOne.T, cmap='ocean')

#/Users/shawnmilloway/Desktop/pic.png
#/Users/shawnmilloway/Desktop/130546838_10225166369855121_5630650196599505556_n.jpeg 
imageImport = Image.open("/Users/shawnmilloway/Desktop/130546838_10225166369855121_5630650196599505556_n.jpeg")
image = np.asarray(imageImport, dtype=np.int64)
image[image == 255] = 1.0
image = grayConversion(image)
imageSize = image.shape
print('imDims', image.shape)


maxIter = 1000; tPlot = 2

nx, ny = imageSize[0], imageSize[1]; ly = ny - 1

xAxis = np.arange(0, nx, 1); yAxis = np.arange(0, ny, 1); X, Y = np.meshgrid(xAxis, yAxis)

uLB = 0.04
omegaOne = 1.0 / (3.0 * (uLB*ny/30.0) + 0.5) 
omegaTwo = 1.0 / (3.0 * (uLB*ny/30.0) + 0.5)
G = -1.2; gOmegaOne = G/omegaOne; gOmegaTwo = G/omegaTwo

v = np.array([[1,1], [1,0], [1,-1], [0,1], [0,0], [0,-1], [-1,1], [-1,0], [-1,-1]])
t = np.array([[1/36], [1/9], [1/36], [1/9], [4/9], [1/9], [1/36], [1/9], [1/36]])

columnZero = np.array([0, 1, 2]); columnOne = np.array([3, 4, 5]); columnTwo = np.array([6, 7, 8])

dRho = 0.001; deltaRho = -dRho * (1.0 - (2.0 * image))
print((deltaRho.max()))

fIn = np.zeros([9, nx, ny]); gIn = np.zeros([9, nx, ny])
for i in range(9):
    fIn[i] = t[i] * (1.0 + deltaRho); gIn[i] = t[i] * (1.0 - deltaRho)

uTotal = np.zeros([2, nx, ny]); rhoOneContrib = np.zeros([2, nx, ny]); rhoTwoContrib = np.zeros([2, nx, ny])
jxOne = np.zeros([2, nx, ny]); jxTwo = np.zeros([2, nx, ny])

fig, ax1 = mplt.subplots(1); mplt.tight_layout(pad=0); fig.set_facecolor('black')
ax1.axis('off'); ax1.set_facecolor('black')

anim = FuncAnimation(fig, animFunc, frames=range(300), interval=1)
anim.save('LBM_PhotoDissolve1.gif', fps=30)


   