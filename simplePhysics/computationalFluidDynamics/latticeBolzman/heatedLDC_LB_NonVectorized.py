import numpy as np
import matplotlib.pyplot as mplt

def collision():
    global u, v, f, fEq, rho, omega, w, cx, cy, n, m, th

    for i in range(n+1):
        for j in range(m+1):
            tOne = u[i,j]**2.0 + v[i,j]**2.0
            for k in range(9):
                tTwo = u[i,j]*cx[k] + v[i,j]*cy[k]
                fEq[k, i, j] = rho[i,j] * w[k] * (1.0 + 3.0*tTwo + 4.5*(tTwo**2.0) - 1.5*tOne)
                f[k, i, j] = omega * fEq[k, i, j] + (1.0 - omega) * f[k, i, j]

def collT():
    global u, v, g, gEq, th, omegaT, w, cx, cy, n, m
    for i in range(n+1):
        for j in range(m+1):
            for k in range(9):
                gEq[k, i, j] = th[i,j] * w[k] * (1.0 + 3.0*(u[i,j]*cx[k] + v[i,j]*cy[k]))
                g[k, i, j] = omegaT*gEq[k, i, j] + (1.0-omegaT)*g[k, i, j]

def streaming(data):
    global n, m

    for j in range(m+1):
        #right to left
        for i in range(n, 0, -1):
            data[1, i, j] = data[1, i-1, j]

        #left to right
        for i in range(n):
            data[3, i, j] = data[3, i+1, j]

    #top to bottom
    for j in range(m, 0, -1):
        for i in range(n+1):
            data[2, i, j] = data[2, i, j-1]
        for i in range(n, 0, -1):
            data[5, i, j] = data[5, i-1, j-1]
        for i in range(n):
            data[6, i, j] = data[6, i+1, j-1]
    
    #bottom to top
    for j in range(m):
        for i in range(n+1):
            data[4, i, j] = data[4, i, j+1]
        for i in range(n):
            data[7, i, j] = data[7, i+1, j+1]
        for i in range(n, 0, -1):
            data[8, i, j] = data[8, i-1, j+1]

def sfBound():
    global f, n, m, uO

    for j in range(m+1):
        #bounce back west boundary
        f[1, 0, j] = f[3, 0, j]
        f[5, 0, j] = f[7, 0, j]
        f[8, 0, j] = f[6, 0, j]
        #bounce back east boundary
        f[3, n, j] = f[1, n, j]
        f[7, n, j] = f[5, n, j]
        f[6, n, j] = f[8, n, j]
    #bounce back south boundary
    for i in range(n+1):
        f[2, i, 0] = f[4, i, 0]
        f[5, i, 0] = f[7, i, 0]
        f[6, i, 0] = f[8, i, 0]
    #moving lid [northern boundary]
    for i in range(1, n):
        rhoN = f[0, i, m] + f[1, i, m] + f[3, i, m] + 2.0*(f[2, i, m] + f[6, i, m] + f[5, i, m])
        f[4, i, m] = f[2, i, m]
        f[8, i, m] = f[6, i, m] + rhoN*uO/6.0
        f[7, i, m] = f[5, i, m] - rhoN*uO/6.0


def gBound():
    global g, tw, w, n, m

    #West Boundary Condition
    for j in range(m+1):
        g[1, 0, j] = -g[3, 0, j]
        g[5, 0, j] = -g[7, 0, j]
        g[8, 0, j] = -g[6, 0, j]
    #East Boundary Condition
    for j in range(m+1):
        g[6, n, j] = -g[8, n, j]
        g[3, n, j] = -g[1, n, j]
        g[7, n, j] = -g[5, n, j]
        g[2, n, j] = -g[4, n, j]
        g[0, n, j] = 0.0
    #Top Boundary Conditions
    for i in range(n+1):
        g[8, i, m] = tw*(w[8] + w[6]) - g[6, i, m]
        g[7, i, m] = tw*(w[7] + w[5]) - g[5, i, m]
        g[4, i, m] = tw*(w[4] + w[2]) - g[2, i, m]
        g[1, i, m] = tw*(w[1] + w[3]) - g[3, i, m]
    #Bottom Boundary Conditions
    for i in range(n+1):
        g[1, i, 0] = g[1, i, 1]
        g[2, i, 0] = g[2, i, 1]
        g[3, i, 0] = g[3, i, 1]
        g[4, i, 0] = g[4, i, 1]
        g[5, i, 0] = g[5, i, 1]
        g[6, i, 0] = g[6, i, 1]
        g[7, i, 0] = g[7, i, 1]
        g[8, i, 0] = g[8, i, 1]

def tCalcu():
    global g, th, n, m

    for j in range(m+1):
        for i in range(n+1):
            sSumT = 0.0
            for k in range(9):
                sSumT += g[k, i, j]
            th[i, j] = sSumT

def rhoUV():
    global f, rho, u, v, cx, cy, n, m

    for j in range(m+1):
        for i in range(n+1):
            sSum = 0.0
            for k in range(9):
                sSum += f[k, i, j]
            rho[i, j] = sSum

    for i in range(1, n+1):
        for j in range(1, m):
            uSum = 0.0; vSum = 0.0
            for k in range(9):
                uSum += f[k, i, j] * cx[k]
                vSum += f[k, i, j] * cy[k]
            u[i, j] = uSum / rho[i, j]
            v[i, j] = vSum / rho[i, j]

def result():
    global u, v, rho, th, uO, n, m, streamFunction

    for i in range(n + 1):
        rhoAV = 0.5*(rho[i-1, 0] + rho[i, 0])
        if(i != 0):
            streamFunction[i, 0] = streamFunction[i - 1, 0] - rhoAV*0.5*(v[i-1, 0] + v[i, 0])
        for j in range(1, m + 1):
            rhoM = 0.5 * (rho[i, j] + rho[i, j-1])
            streamFunction[i, j] = streamFunction[i, j-1] + rhoM*0.5*(u[i, j-1] + u[i, j])


n = 20; m = 20

f = np.zeros([9, n + 1, m + 1]); fEq = np.zeros_like(f); g = np.zeros_like(f); gEq = np.zeros_like(f)
u = np.zeros([n + 1, m + 1]); v = np.zeros_like(u); rho = np.zeros_like(u); streamFunction = np.zeros_like(u); th = np.zeros_like(u)

cx = [0.0, 1.0, 0.0, -1.0, 0.0, 1.0, -1.0, -1.0, 1.0]
cy = [0.0, 0.0, 1.0, 0.0, -1.0, 1.0,  1.0, -1.0, -1.0]
w = [4./9., 1./9., 1./9., 1./9., 1./9., 1./36., 1./36., 1./36., 1./36.]
print(w)

rhoO = 5.0; uO = 0.2; sumVelo = 0.0
dx = 1.0; dy = dx; dt = 1.0

tw = 1.0; pr = 0.71; visco = 0.02; alpha = visco/pr; Re = uO*m/alpha
omega = 1.0/(3.0 * visco + 0.5); omegaT = 1.0/(3.0 * alpha + 0.5)
mStep = 10000

for j in range(m + 1):
    for i in range(n + 1):
        rho[i, j] = rhoO

for i in range(1, n):
    u[i, m] = uO

for kk in range(1, mStep):

    collision()
    streaming(f)
    sfBound()
    rhoUV()

    tCalcu()
    
    collT()
    streaming(g)
    gBound()

result()

X, Y = np.meshgrid(np.arange(0, n + 1), np.arange(0, m + 1))

mplt.contourf(X, Y, np.sum(g, axis=0))
mplt.show()
