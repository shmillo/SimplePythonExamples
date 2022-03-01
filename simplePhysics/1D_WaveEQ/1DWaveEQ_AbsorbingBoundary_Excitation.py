import importlib
from cmath import cos, exp, log, log10, pi, sin
import matplotlib.pyplot as mplt

#length of simulation space
Lx = 10
#spatial sampling
dx = 0.1 

#number of sample points = Length * spatial sampling
nx = int( Lx / dx )
print(nx)
#compute middle for sources and excitation
middle = int( nx * 0.5 )
#NX linearly spaced values ranging from 0.0 to LX
x = range(0, Lx, nx)

#totalNumberOfSecondsInSimulation
T = 3.0

#set up matrices with size NX - 1
wn = [0.0] * nx
wnp1 = [0.0] * nx
wnm1 = [0.0] * nx

#courant number = c * dt/dx
CFL = 1.0 
c = 1.0
dt = CFL*dx/c

#simple excitation model
wn[middle - 1] = 0.45
wn[middle] = 0.9
wn[middle + 1] = 0.45

wnp1[middle - 1] = 0.45
wnp1[middle] = 0.9
wnp1[middle + 1] = 0.45

#initialize time
t = 0

fig, (ax1, ax2, ax3, ax4, ax5) = mplt.subplots(5, sharex=True, sharey=True)
ax1.axis([ 0, 100, -1.0, 1.0])

ax1.plot(wnp1)

while t < T:

    #reflecting boundary condition
    #wn[0] = 0.0; wn[nx - 1] = 0.0

    #absborbing boundary condition
    wnp1[0] = wn[1] + ((CFL - 1) / (CFL + 1)) * (wnp1[1] - wn[0])
    wnp1[nx - 1] = wn[nx - 2] + ((CFL - 1) / (CFL + 1)) * (wnp1[nx - 2] - wn[nx - 1])

    t += dt
    for i in range(nx - 1):
        wnm1[i] = wn[i]
        wn[i] = wnp1[i]

    for i in range(1, nx - 2):
        wnp1[i] = 2.0*wn[i] - wnm1[i] + CFL**2.0 * (wn[i + 1] - 2.0*wn[i] + wn[i - 1])
    
    if t == 0.1:
        ax2.plot(wnp1)
    elif t == 0.2:
        ax3.plot(wnp1)
    elif t == 0.4:
        ax4.plot(wnp1)
    
        
ax5.plot(wnp1)

print(wnp1[middle])
mplt.show()
