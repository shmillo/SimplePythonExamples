import numpy as np
import matplotlib.pyplot as mplt

def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

plotEvery = 100

Nx = 400; Ny = 100
tau = 0.63
Nt = 6000

Nl = 9
cxs = np.array([0, 0, 1, 1, 1, 0, -1, -1, -1])
cys = np.array([0, 1, 1, 0, -1, -1, -1, 0, 1])
weights = np.array([4/9, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36, 1/9, 1/36])

F = np.ones([Ny, Nx, Nl]) + 0.1 * np.random.randn(Ny, Nx, Nl)
F[:, :, 3] = 2.3

cylinders = np.full((Ny, Nx), False)
locationsX = [200, 140, 50, 20, 300]
locationsY = [50, 30, 80, 13, 70]

for y in range(0, Ny):
    for x in range(0, Nx):
        for l in range(len(locationsX)):
                if(distance(locationsX[l], locationsY[l], x, y) < 13):
                    cylinders[y][x] = True
                    print(y, x)


for it in range(Nt):

    F[:, -1, [6, 7, 8]] = F[:, -2, [6, 7, 8]]
    F[:, 0, [2, 3, 4]] = F[:, 1, [2, 3, 4]]

    for i, cx, cy in zip(range(Nl), cxs, cys):
        F[:, :, i] = np.roll(F[:, :, i], cx, axis=1)
        F[:, :, i] = np.roll(F[:, :, i], cy, axis=0)
    
    boundaryF = F[cylinders, :]
    boundaryF = boundaryF[:, [0, 5, 6, 7, 8, 1, 2, 3, 4]]

    rho = np.sum(F, 2)
    ux = np.sum(F * cxs, 2) / rho; uy = np.sum(F * cys, 2) / rho

    F[cylinders, :] = boundaryF
    ux[cylinders] = 0; uy[cylinders] = 0

    Feq = np.zeros(F.shape)
    for i, cx, cy, w in zip(range(Nl), cxs, cys, weights):
        Feq[:, :, i] = rho * w * (1 + 3 * (cx*ux + cy*uy) + 9 * (cx*ux + cy*uy)**2 / 2 - 3 * (ux**2 + uy**2) / 2)
    F = F + -(1/tau) * (F - Feq)

    if(it%plotEvery == 0):
        dfydx = ux[2:, 1:-1] - ux[0:-2, 1:-1]
        dfxdy = uy[1:-1, 2:] - uy[1:-1, 0:-2]
        mplt.imshow(dfydx - dfxdy, cmap='bwr')
        #mplt.imshow(np.sqrt(ux**2 + uy**2))
        mplt.pause(0.01)
        mplt.cla()

dfydx = ux[2:, 1:-1] - ux[0:-2, 1:-1]
dfxdy = uy[1:-1, 2:] - uy[1:-1, 0:-2]
mplt.imshow(dfydx - dfxdy, cmap='bwr')
mplt.show()