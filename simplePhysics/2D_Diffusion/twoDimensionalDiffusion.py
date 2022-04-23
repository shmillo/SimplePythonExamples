import numpy as np
import matplotlib.pyplot as mplt

#grid information
Lx = 10; Ly = 10
Nx = 51; Ny = 51; Nt = 500
dx = Lx/(Nx - 1); dy = Ly/(Ny - 1)
rho = 1; cp = 1
c = 1; C = 0.05; dt = C*dx/c

#initialize mats to correct sizes
Tc = [ [0.0] * Ny for _ in range(Nx) ]
Tn = [ [0.0] * Ny for _ in range(Nx) ]
k = [ [1.0] * Ny for _ in range(Nx) ]

#place initial source
for i in range(20, 25):
    for j in range( 30, 35):
        k[i][j] = 0.0001 #square hole - thermal conductivity is very low

#Source Term / Location of Source
Sx = round(7.0*Nx/Lx); Sy = round(3.0*Ny/Ly)

t = 0; 
for n in range( 0, Nt ):
    
    Tc = Tn #copy old temps for new time step
    
    for i in range( 1, Nx - 1 ):
        for j in range( 1, Ny - 1 ):
            #five point stencil with forcing function that includes the source
            Tn[j][i] = Tc[j][i] + dt * (k[j][i]/rho/cp) * ((Tc[j][i+1] + Tc[j+1][i] - 4.0*Tc[j][i] + Tc[j][i-1] + Tc[j-1][i])/dx/dx)
    
    t = t + dt #inc time

    if(t < 1):
        #the source turns off at t == 1
        Tn[Sy][Sx] = Tn[Sy][Sx] + dt*100/rho/cp; 

    #mixed boundary conditions
    for i in range(Nx): 
        Tn[0][i] = 0.0
        Tn[Ny - 1][i] = 0.0
        Tn[i][0] = 0
        Tn[i][Ny - 1] = Tn[i][Ny - 2]; 


mplt.contour(Tn)
mplt.show()