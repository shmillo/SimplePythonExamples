import numpy as np
import matplotlib.pyplot as mplt

def invel(uLB, ly):
    def inner(d, x, y):
        return (1.0 - d) * uLB * (1.0 + 1.0e-4*np.sin(y/ly*2.0*np.pi))
    return inner

def macroscopic(xIn, nx, ny, v):
    rho = np.sum(xIn, axis=0)
    u = np.zeros([2, nx, ny])
    for i in range(9):
        u[0, :, :] += v[i, 0] * xIn[i, :, :]
        u[1, :, :] += v[i, 1] * xIn[i, :, :]
    u /= rho
    return rho, u

def unNormalizedMacroscopic(xIn, nx, ny, v):
    rho = np.sum(xIn, axis=0)
    u = np.zeros([2, nx, ny])
    for i in range(9):
        u[0, :, :] += v[i, 0] * xIn[i, :, :]
        u[1, :, :] += v[i, 1] * xIn[i, :, :]
    return rho, u

def macroscopic2PhaseFlow():
    global rhoOne, rhoTwo, v, nx, ny, v, omegaOne, omegaTwo, fIn, gIn
    
    rhoOne = np.sum(fIn, axis=0); rhoTwo = np.sum(gIn, axis=0)
    jxOne = np.zeros([2, nx, ny]); jxTwo = np.zeros([2, nx, ny])
    for i in range(9):
        jxOne[0, :, :] += v[i, 0] * fIn[i, :, :]
        jxOne[1, :, :] += v[i, 1] * fIn[i, :, :]

        jxTwo[0, :, :] += v[i, 0] * gIn[i, :, :]
        jxTwo[1, :, :] += v[i, 1] * gIn[i, :, :]

    rhoTotOmega = rhoOne*omegaOne + rhoTwo*omegaTwo
    uTotal = (jxOne*omegaOne + jxTwo*omegaTwo)/rhoTotOmega

    return rhoOne, rhoTwo, uTotal

def equilibrium(rho, u, v, t, nx, ny):
    usqr = (3.0/2.0) * (u[0]**2.0 + u[1]**2.0)
    xEq = np.zeros([9, nx, ny])
    for i in range(9):
        cu = 3.0*((v[i, 0]*u[0, :, :]) + (v[i, 1]*u[1, :, :]))
        xEq[i, :, :] = rho * t[i] * (1.0 + cu + 0.5*cu**2.0 - usqr)
    return xEq
    
Re = 9.0
maxIter = 1000; tPlot = 2

G = -1.2; omegaOne = 1.0; omegaTwo = 1.0; gOmegaOne = G/omegaOne; gOmegaTwo = G/omegaTwo

nx, ny = 201, 201; ly = ny - 1
cx, cy, r = nx//4, ny//2, ny/9
xAxis = np.arange(0, nx, 1); yAxis = np.arange(0, ny, 1); X, Y = np.meshgrid(xAxis, yAxis)

uLB = 0.04
nulb = uLB*ny/Re
omega = 1.0/(3.0*nulb + 0.5)

v = np.array([[1,1], [1,0], [1,-1], [0,1], [0,0], [0,-1], [-1,1], [-1,0], [-1,-1]])
t = np.array([[1/36], [1/9], [1/36], [1/9], [4/9], [1/9], [1/36], [1/9], [1/36]])
columnZero = np.array([0, 1, 2]); columnOne = np.array([3, 4, 5]); columnTwo = np.array([6, 7, 8])

dRho = 0.001; deltaRho = -dRho * (1.0 - (2.0 * np.random.rand(nx, ny)))

velocity = np.fromfunction(invel(uLB, ly), (2, nx, ny))
fIn = np.zeros([9, nx, ny]); gIn = np.zeros([9, nx, ny])
for i in range(9):
    fIn[i] = t[i] * (1.0 + deltaRho); gIn[i] = t[i] * (1.0 - deltaRho)

uTotal = np.zeros([2, nx, ny])
rhoOneContrib = np.zeros([2, nx, ny]); rhoTwoContrib = np.zeros([2, nx, ny])

for cycle in range(maxIter):

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

    if( (cycle%tPlot) == 0.0 ):
        mplt.imshow(rhoOne.T, cmap='prism')
        #mplt.scatter(X, Y, rhoTwo, c=rhoTwo)
        mplt.draw()
        mplt.pause(0.03)
        mplt.cla()
