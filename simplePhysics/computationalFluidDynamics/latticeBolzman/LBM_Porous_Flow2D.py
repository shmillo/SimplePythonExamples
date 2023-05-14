import numpy as np
import matplotlib.pyplot as mplt

nx = 31; ny = 31
omega = 1.0; density = 1.0; t1 = 4.0/9.0; t2 = 1.0/9.0; t3 = 1.0/36.0; cSq = 1.0/3.0; dU = 1.0e-7

F = np.ones([nx, ny, 9]); F *= density/9.0; Feq = np.zeros_like(F)

BOUND = np.random.rand(nx, ny); BOUND[BOUND > 0.6] = 1.0; BOUND[BOUND != 1.0] = 0.0
boundIndices = np.nonzero(BOUND)
print(boundIndices[0])
print(boundIndices[1])

reflectOrder = [0, 1, 2, 3, 4, 5, 6, 7]; reflectedOrder = [4, 5, 6, 7, 0, 1, 2, 3]

toReflect = np.zeros_like(F)
for i in range(9):
    toReflect[:, :, i] = np.copy(BOUND)
reflected = np.copy(toReflect)

bouncedBack = np.zeros_like(F)

indicesOne = np.array(range(1, nx + 1), dtype=np.int8); indicesOne = indicesOne%nx
indicesTwo = np.array(range(ny - 1, ny*2 - 1), dtype=np.int8); indicesTwo = indicesTwo%ny
indicesThree = np.array(range(nx - 1, nx*2 - 1), dtype=np.int8); indicesThree = indicesThree%nx
indicesFour = np.array(range(1, ny + 1), dtype=np.int8); indicesFour = indicesFour%ny

for j in range(100):

    #propogation Step
    F[:, :, 3] = F[indicesOne, indicesTwo, 3]
    F[:, :, 2] = F[:, indicesTwo, 2]
    F[:, :, 1] = F[indicesThree, indicesTwo, 1]
    F[:, :, 4] = F[indicesOne, :, 4]
    F[:, :, 0] = F[indicesThree, :, 0]
    F[:, :, 5] = F[indicesOne, indicesFour, 5]
    F[:, :, 6] = F[:, indicesFour, 6]
    F[:, :, 7] = F[indicesThree, indicesFour, 7]

    #save densities to reflect at next time step
    bouncedBack.fill(0.0)
    for i in reflectOrder:
        #bouncedBack[BOUND == 1.0, i] = F[BOUND == 1.0, i]
        bouncedBack[boundIndices[0], boundIndices[1], i] = F[boundIndices[0], boundIndices[1], i] 

    DENSITY = np.sum(F, 2)
    uX = ( np.sum(F[:, :, [1, 2, 8]], 2) - np.sum(F[:, :, [4, 5, 6]], 2) ) / DENSITY
    uY = ( np.sum(F[:, :, [2, 3, 4]], 2) - np.sum(F[:, :, [6, 7, 8]], 2) ) / DENSITY
 
    #Boundary conditions
    #increase inlet pressure over time
    uX[0, :] += dU
    #set obstacle densities and velocities to 0.0
    #uX[BOUND == 1.0] = 0.0; uY[BOUND == 1.0] = 0.0; DENSITY[BOUND == 1.0] = 0.0
    uX[boundIndices[0], boundIndices[1]] = 0.0; uY[boundIndices[0], boundIndices[1]] = 0.0; DENSITY[boundIndices[0], boundIndices[1]] = 0.0

    #constants for Equillibrium calculation
    uSq = uX**2.0 + uY**2.0; uSqTemp = uSq/(2.0*cSq)
    uC2 = uX + uY; uC4 = uY - uX; uC6 = -1.0*uC2; uC8 = -1.0*uC4

    #Center equillibrium
    Feq[:, :, 8] = t1 * DENSITY * (1.0 - uSqTemp)
    #Nearest neighbors
    tDENSITY = t2 * DENSITY
    feqX = tDENSITY * (1.0 + uX/cSq + 0.5*(uX/cSq)**2.0 - uSqTemp)
    feqY = tDENSITY * (1.0 - uY/cSq + 0.5*(uY/cSq)**2.0 - uSqTemp)
    Feq[:, :, 0] = feqX; Feq[:, :, 2] = feqX
    Feq[:, :, 4] = feqY; Feq[:, :, 6] = feqY
    #Next-nearest
    tDENSITY = t3 * DENSITY
    Feq[:, :, 1] = tDENSITY * (1.0 + uC2/cSq + 0.5*(uC2/cSq)**2.0 - uSqTemp)
    Feq[:, :, 3] = tDENSITY * (1.0 + uC4/cSq + 0.5*(uC4/cSq)**2.0 - uSqTemp)
    Feq[:, :, 5] = tDENSITY * (1.0 + uC6/cSq + 0.5*(uC6/cSq)**2.0 - uSqTemp)
    Feq[:, :, 7] = tDENSITY * (1.0 + uC8/cSq + 0.5*(uC8/cSq)**2.0 - uSqTemp)
    #relaxation towards equillibrium
    F = omega*Feq + (1.0 - omega)*F

    for i in range(8):
        F[boundIndices[0], boundIndices[1], reflectedOrder[i]] = bouncedBack[boundIndices[0], boundIndices[1], reflectOrder[i]] 
    
    print(j)

X, Y = np.meshgrid(range(nx), range(ny))

print(uX)

mplt.quiver(range(2,nx), range(ny), uX[2:nx, :].T, uY[2:ny, :].T)
mplt.show()