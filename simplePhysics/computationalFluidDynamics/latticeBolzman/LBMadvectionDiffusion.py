import numpy as np
import matplotlib.pyplot as mplt

nodes = [100, 100]
u = 2.71; v = 1.4
dh = 1; dt = 1
timesteps = 400
alpha = 1.0; twall = 1.0

w = np.array([4/9, 1/9, 1/9, 1/9, 1/9, 1/36, 1/36, 1/36, 1/36])
L = dh * [nodes[0] - 1, nodes[1] - 1]
ck = dh/dt; csq = ck**2.0; omega = 1.0/(3.0*alpha/(dt*csq)+0.5)

x = np.linspace(0, L[0], num=nodes[0]); y = np.linspace(0, L[1], num=nodes[1])
f = np.zeros([nodes[1], nodes[0], 9]); feq = np.zeros([nodes[1], nodes[0], 9])
for k in range(9):
    f[:, 0, k] = w[k] * twall

for i in range(timesteps):

    rho = np.sum(f, axis=2)

    feq[:, :, 0] = w[0] * rho
    feq[:, :, 1] = w[1] * rho * (1.0 + 3.0*u/ck)
    feq[:, :, 2] = w[2] * rho * (1.0 + 3.0*v/ck)
    feq[:, :, 3] = w[3] * rho * (1.0 - 3.0*u/ck)
    feq[:, :, 4] = w[4] * rho * (1.0 - 3.0*v/ck)
    feq[:, :, 5] = w[5] * rho * (1.0 + 3.0*(u+v)/ck)
    feq[:, :, 6] = w[6] * rho * (1.0 + 3.0*(-u+v)/ck)
    feq[:, :, 7] = w[7] * rho * (1.0 - 3.0*(u+v)/ck)
    feq[:, :, 8] = w[8] * rho * (1.0 + 3.0*(u-v)/ck)
    for k in range(9):
        f[:, :, k] = omega * feq[:, :, k] + (1.0 - omega) * f[:, :, k]
    
    end = f.shape[0]
    f[:, 1:end-1, 1] = f[:, :end-2, 1] #eastern stream
    f[1:end-1, :, 2] = f[:end-2, :, 2] #northern
    f[:, :end-2, 3] = f[:, 1:end-1, 3] #western
    f[:end-2, :, 4] = f[1:end-1, :, 4] #southern
    f[1:end-1, 1:end-1, 5] = f[:end-2, :end-2, 5] #northeastern
    f[1:end-1, :end-2, 6] = f[:end-2, 1:end-1, 6] #northwestern
    f[:end-2, :end-2, 7] = f[1:end-1, 1:end-1, 7] #southwest
    f[:end-2, 1:end-1, 8] = f[1:end-1, :end-2, 8] #southeast

    f[:, 0, 1] = w[1]*twall + w[3]*twall - f[:, 0, 3] # Left boundary, T = 1.0.
    f[:, 0, 5] = w[5]*twall + w[7]*twall - f[:, 0, 7] # Left boundary, T = 1.0.
    f[:, 0, 8] = w[8]*twall + w[6]*twall - f[:, 0, 6] # Left boundary, T = 1.0.
    
    f[:, end-1, 3] = -f[:, end-1, 1] # Right boundary, T = 0.
    f[:, end-1, 6] = -f[:, end-1, 8] # Right boundary, T = 0.
    f[:, end-1, 7] = -f[:, end-1, 5] # Right boundary, T = 0.
    f[:, end-1, 2] = -f[:, end-1, 4] # Right boundary, T = 0.
    f[:, end-1, 0] = 0 # Right boundary, T = 0.
    
    f[end-1, :, 4] = -f[end-1, :, 2] # Top boundary, T = 0.
    f[end-1, :, 7] = -f[end-1, :, 5] # Top boundary, T = 0.
    f[end-1, :, 8] = -f[end-1, :, 6] # Top boundary, T = 0.
    f[end-1, :, 1] = -f[end-1, :, 3] # Top boundary, T = 0.
    f[end-1, :, 0] = 0 # Top boundary, T = 0.
    
    #for k in range(1, 9):
        #f(1,:,k) = f(2,:,k); % Bottom boundary, adiabatic.
    f[0, :, 2] = -f[0, :, 4] # Bottom boundary, T = 0.
    f[0, :, 6] = -f[0, :, 8] # Bottom boundary, T = 0.
    f[0, :, 5] = -f[0, :, 7] # Bottom boundary, T = 0.
    f[0, :, 1] = -f[0, :, 3] # Bottom boundary, T = 0.
    f[0, :, 0] = 0 # Bottom boundary, T = 0.

    [X, Y] = np.meshgrid(x,y)
    mplt.contour(X, Y, rho)
    
    mplt.draw()
    mplt.pause(0.01)
    mplt.cla()
mplt.show()