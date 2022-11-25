from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as mplt
import numpy as np

def diffuse(b, x, x0, diff):
    global Nx, Ny, dt
    a = dt * diff * (Nx - 2) * (Ny - 2)
    lin_solve(b, x, x0, a, 1 + 6 * a)

def lin_solve(b, x, x0, a, c):
    global iter
    cRecip = 1.0 / c
    for k in range(0, iter):
        for j in range(1, Ny - 1):
            for i in range(1, Nx - 1):
                x[IX(i, j)] = (x0[IX(i, j)] + a*(x[IX(i+1,j)] + x[IX(i-1,j)] + x[IX(i,j+1)] + x[IX(i,j-1)])) * cRecip

def project(velocX, velocY, p, div):
    global Nx, Ny
    for j in range(1, Ny - 1):
        for i in range(1, Nx - 1):
            div[IX(i, j)] = -0.5 * ((velocX[IX(i+1, j)]-velocX[IX(i-1, j)])/Nx + (velocY[IX(i, j+1)]-velocY[IX(i, j-1)])/Ny)
            p[IX(i, j)] = 0

    set_bnd(0, div); set_bnd(0, p); lin_solve(0, p, div, 1, 6)

    for j in range(1, Ny - 1):
        for i in range(1, Nx - 1):
            velocX[IX(i, j)] -= 0.5 * (p[IX(i+1, j)] - p[IX(i-1, j)]) * Nx
            velocY[IX(i, j)] -= 0.5 * (p[IX(i, j+1)] - p[IX(i, j-1)]) * Ny

    set_bnd(1, velocX); set_bnd(2, velocY)

def advect(b, d, d0, velocX, velocY):
    global Ny, Nx, dt

    i0 = 0; i1 = 0; j0 = 0; j1 = 0
    dtx = dt * (Nx - 2); dty = dt * (Ny - 2)
    s0 = 0; s1 = 0; t0 = 0; t1 = 0; tmp1 = 0; tmp2 = 0; x = 0; y = 0
    Nxfloat = Nx; Nyfloat = Ny; ifloat = 1.0; jfloat = 1.0; i = 0; j = 0
  
    for j in range(1, Ny - 1): 
        ifloat = 1
        for i in range(1,  Nx - 1):
            
            tmp1 = dtx * velocX[IX(i, j)]; tmp2 = dty * velocY[IX(i, j)]
            x = ifloat - tmp1; y = jfloat - tmp2

            if (x < 0.5): x = 0.5 
            if (x > Nxfloat + 0.5): x = Nxfloat + 0.5; 
            i0 = int(x); i1 = i0 + 1.0

            if (y < 0.5): y = 0.5; 
            if (y > Nyfloat + 0.5): y = Nyfloat + 0.5; 
            j0 = int(y); j1 = j0 + 1.0; 

            s1 = x - i0; s0 = 1.0 - s1 
            t1 = y - j0; t0 = 1.0 - t1

            i0i = int(i0); i1i = int(i1)
            j0i = int(j0); j1i = int(j1)

            d[IX(i, j)] = (s0 * (t0 * d0[IX(i0i, j0i)] + t1*d0[IX(i0i, j1i)])) + (s1*(t0*d0[IX(i1i, j0i)] + t1*d0[IX(i1i, j1i)]))
            ifloat = ifloat + 1
        jfloat = jfloat + 1

def constrain(value, bound1, bound2):
    global Ny, Nx

    returnValue = 0
    if(value < bound1): 
        returnValue = bound1
    elif(value > bound2):
        returnValue = bound2
    else:
        returnValue = value
    return returnValue

def IX(x, y):
    global Ny, Nx
    x = constrain(x, 0, Nx-1); y = constrain(y, 0, Ny-1); returnValue = x + (y * Nx)
    return returnValue 

def set_bnd(b, x):
    global Ny, Nx

    #1, Nx-1
    for i in range(1, Nx):
        x[IX(i, 0)] = -x[IX(i, 1)] if b == 2 else x[IX(i, 1)]
        x[IX(i, Ny-1)] = -x[IX(i, Ny-2)] if b == 2 else x[IX(i, Ny-2)]
  
    #1, Ny-1
    for j in range(1, Ny): 
        x[IX(0, j)] = -x[IX(1, j)] if b == 1 else x[IX(1, j)]
        x[IX(Nx-1, j)] = -x[IX(Nx-2, j)] if b == 1 else x[IX(Nx-2, j)]

    x[IX(0, 0)] = 0.5 * (x[IX(1, 0)] + x[IX(0, 1)])
    x[IX(0, Ny-1)] = 0.5 * (x[IX(1, Ny-1)] + x[IX(0, Ny-2)])
    x[IX(Nx-1, 0)] = 0.5 * (x[IX(Nx-2, 0)] + x[IX(Nx-1, 1)])
    x[IX(Nx-1, Ny-1)] = 0.5 * (x[IX(Nx-2, Ny-1)] + x[IX(Nx-1, Ny-2)])

def addVelocity(x, y, amountX, amountY):
    global Vy, Vx
    index = IX(x, y)
    Vx[index] += amountX; Vy[index] += amountY
  
def addDensity(x, y, amount):
    global density
    index = IX(x, y)
    density[index] += amount

def step(i):
    global Vx0, Vx, viscosity, dt, s, xAxis, yAxis, X, Y, pX, pY, totalNumFrames

    pointX = []; pointY = []; centerX = int(Nx * 0.5); centerY = int(Ny * 0.5)
    randomRadius = 16.0; randomCenter = randomRadius * 0.5; circularPeriod = totalNumFrames * 0.1

    sourceEnvelope = np.exp(20.0 * (-i/totalNumFrames))
    pointX.append(int(constrain(sourceEnvelope * (centerX + (16.0 * np.cos((i + 2000)/circularPeriod))), 0, Nx*0.66))) 
    pointX.append(int(constrain(Nx*0.66 + (16.0 * np.cos((i - 2000)/circularPeriod)), 0, Nx*0.80)))
    
    pointY.append(int(constrain(sourceEnvelope * (centerY + (16.0 * np.cos((i + 2000)/circularPeriod))), 0, Ny*0.66)))
    pointY.append(int(constrain(Nx*0.66 + (16.0 * np.sin((i - 2000)/circularPeriod)), 0, Ny*0.8)))

    numPointsSurrounding = 10; velocityX = 1.0; velocityY = 0.10; densityX = 0.10; densityY = 5.0
    for h in range(len(pointX)):
        for j in range(numPointsSurrounding):
            for q in range(numPointsSurrounding):
                addDensity(pointX[h] + j, pointY[h] + q, densityX); addVelocity(pointX[h] + j, pointY[h] + q, velocityX, velocityY )

    diffuse(1, Vx0, Vx, viscosity); diffuse(2, Vy0, Vy, viscosity)
    advect(1, Vx, Vx0, Vx0, Vy0); advect(2, Vy, Vy0, Vx0, Vy0)

    project(Vx, Vy, Vx0, Vy0)

    plotX = [ [0.0] * Ny for _ in range(Nx) ]; plotY = [ [0.0] * Ny for _ in range(Nx) ]
    for i in range(Nx):
        for j in range(Ny):
            plotX[i][j] = Vx[IX(i,j)]; plotY[i][j] = Vy[IX(i,j)]
            Vx0[IX(i,j)] = Vx[IX(i,j)]; Vy0[IX(i,j)] = Vy[IX(i,j)]

    mplt.contourf(X, Y, plotX, cmap='ocean')
    
Nx = 268; Ny = 268; iter = 10; dt = 0.05; diffusion = 10.051; 
viscosity = 0.0501; pX = 0.0; pY = 0.0; totalNumFrames = 10000

Vx = [ 0.0 ] * (Nx*Ny); Vy = [ 0.0 ] * (Nx*Ny); Vx0 = [ 0.0 ] * (Nx*Ny); Vy0 = [ 0.0 ] * (Nx*Ny)
s = [ 0.0 ] * (Nx*Ny); density = [ 0.0 ] * (Nx*Ny)
xAxis = np.linspace(0, Nx, num=Nx); yAxis = np.linspace(0, Ny, num=Nx); X,Y = np.meshgrid(xAxis, yAxis)

fig, ax = mplt.subplots(1,1)
anim = FuncAnimation(fig, func=step, frames=np.linspace(0, totalNumFrames), interval=100)
anim.save('fluidSim_T1.gif')
mplt.show()