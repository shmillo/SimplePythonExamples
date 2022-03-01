import importlib
from cmath import cos, exp, log, log10, pi, sin
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as mplt

########### ########### ########### ########### ###########
########### ########### ########### ########### ###########

#length of simulation space
Lx = 10
Ly = 10

#spatial sampling
dx = 0.1 
dy = dx

#number of sample points = Length * spatial sampling
nx = int( Lx / dx )
ny = int( Ly / dx )

#compute middle for sources and excitation
middleX = int( nx * 0.5 )
middleY = int( ny * 0.5 )

#totalNumberOfSecondsInSimulation
T = 30.0

########### ########### ########### ########### ###########
########### ########### ########### ########### ###########

#set up matrices with size NX - 1
wn = [[0.0]*nx for _ in range(ny)]
wnp1 = [[0.0]*nx for _ in range(ny)]
wnm1 = [[0.0]*nx for _ in range(ny)]

########### ########### ########### ########### ###########
########### ########### ########### ########### ###########

#courant number = c * dt/dx
CFL = 0.5 
#propogation speed
c = 1.0
dt = CFL*dx/c

########### ########### ########### ########### ###########
########### ########### ########### ########### ###########

#NX linearly spaced values ranging from 0.0 to LX
Xs = range(0, nx)
Ys = range(0, nx)

fig = mplt.figure()
ax = fig.gca(projection = '3d')

########### ########### ########### ########### ###########
########### ########### ########### ########### ###########

#initialize time
t = 0
#advance time
while t < T:

    #reflecting boundary condition
    for i in range(nx - 1):
        
        wn[0][i] = 0.0; wn[nx - 1][0] = 0.0

    #absborbing boundary condition
    #wnp1[0] = wn[1] + ((CFL - 1) / (CFL + 1)) * (wnp1[1] - wn[0])
    #wnp1[nx - 1] = wn[nx - 2] + ((CFL - 1) / (CFL + 1)) * (wnp1[nx - 2] - wn[nx - 1])

    #advance time for real
    t += dt

    #update memory
    for i in range(nx - 1):
        for j in range(ny - 1):
            wnm1[i][j] = wn[i][j]
            wn[i][j] = wnp1[i][j]

    #Source
    wn[middleX][middleY] = dt**2.0 * 20.0*sin(30.0 * pi * t/20.0).real

    for i in range(1, nx - 2):
        for j in range(1, ny - 2):
            temporary =  CFL**2.0 * ( wn[i+1][j] + wn[i][j+1] - 4.0*wn[i][j] + wn[i - 1][j] + wn[i][j-1] )
            wnp1[i][j] = 2.0*wn[i][j] - wnm1[i][j] + temporary

  

########### ########### ########### ########### ###########
########### ########### ########### ########### ###########

#actual values to plot (heighths of the graph interpolated against grid [X,Y])
Zs = wnp1
mplt.axis('off')
ax.contour(Xs, Ys, Zs)
mplt.show()
    

