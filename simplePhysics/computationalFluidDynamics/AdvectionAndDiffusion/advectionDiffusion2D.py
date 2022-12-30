import numpy as np
import matplotlib.pyplot as mplt

def stream2d(F, vector):

    # Matlab equivalent solution:    
    # F = circshift(A,[y,x])
    A = np.copy(F)
    y = vector[0]; x = vector[1]; m, n = A.shape
    b = np.zeros([1, n]); c = np.zeros([m, 1])

    if(x == 1):    # x+ stream
        b = A[:, n-1]
        for i in range(n-1, 0, -1):
            A[:, i] = A[:, i-1]
        A[:, 0] = b
    elif(x == -1):  # x- stream
        b = A[:, 0]
        for i in range(n-1):
            A[:, i] = A[:, i+1]
        A[:, n-1] = b

    if(y == 1):      # y+ stream
        c = A[m-1, :]
        for j in range(m-1, 0, -1):
            A[j, :] = A[j-1, :]
        A[0, :] = c
    elif(y == -1):  # y- stream
        c = A[0, :]
        for j in range(m-1):
            A[j, :] = A[j+1, :]
        A[m-1, :] = c

    return A

L = 10; H = 10; n = 10; m = 10
dx = L/n; dy = H/m; dt = 1; K = 9
#x = np.linspace(1, L, num=int(L*dx)); y = np.linspace(1, H, num=int(H*dy))

f = np.zeros([m, n, K]); rho = np.zeros([m, n]); fEq = np.zeros([m, n])

csq = (dx**2.0 / dt**2.0); alpha = 0.25; omega = 1.0/(3.0*alpha/(csq*dt) + 0.5)

w = np.array([4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36])
C = np.array([[0,0], [1,0], [0,1], [-1,0], [0,-1], [1,1], [-1,1], [-1,-1], [1,-1]])
links = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
tEnd = 1000; tPlot = 10; frames = tEnd/tPlot; count = 0
print(C[1][0], C[1][1])

print(w.shape, C.shape, links.shape)

tWall = 1
for k in range(links.shape[0]):
    if(k == 0):
        continue
    elif(k != 0):
        f[:, :, k] = w[k] * rho

rho = np.zeros([n, m])
for cycle in range(tEnd):
    
    for k in range(links.shape[0]):
        rho += f[:, :, k]

    for k in range(links.shape[0]):
        fEq = w[k] * rho
        f[:, :, k] = omega*fEq + (1.0 - omega)*f[:, :, k]

    for k in range(links.shape[0]):
        f[:, :, k] = stream2d(f[:, :, k], [C[k][1], C[k][0]])
    
    f[:, 0, 1] = w[1]*tWall + w[3]*tWall - f[:, 0, 3]
    f[:, 0, 5] = w[5]*tWall + w[7]*tWall - f[:, 0, 7]
    f[:, 0, 8] = w[8]*tWall + w[6]*tWall - f[:, 0, 6]

    f[:, n-1, 3] = -f[:, n-1, 1]
    f[:, n-1, 6] = -f[:, n-1, 8]
    f[:, n-1, 7] = -f[:, n-1, 5]

    f[m-1, :, 7] = -f[m-1, :, 5]
    f[m-1, :, 4] = -f[m-1, :, 2]
    f[m-1, :, 8] = -f[m-1, :, 6]

    f[0, :, 0] = f[1, :, 0]
    f[0, :, 1] = f[1, :, 1]
    f[0, :, 2] = f[1, :, 2]
    f[0, :, 3] = f[1, :, 3]
    f[0, :, 4] = f[1, :, 4]
    f[0, :, 5] = f[1, :, 5]
    f[0, :, 6] = f[1, :, 6]
    f[0, :, 7] = f[1, :, 7]
    f[0, :, 8] = f[1, :, 8]
    
    if(cycle%tPlot == 0.0):
        mplt.contourf(rho)
        mplt.draw()
        mplt.pause(0.01)
        mplt.cla()
