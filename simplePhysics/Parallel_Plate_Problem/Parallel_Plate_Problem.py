from cmath import pi, sin, sqrt
import numpy as np
from math import ceil, floor
import matplotlib.pyplot as mplt

def matrixTranspose(A):
    B = [ [A[j][i] for j in range(len(A))] for i in range(len(A[0])) ]
    return B

#dimensions
Nx = 21          #Number of X-grids
Ny = 21          #Number of Y-grids
mpx = ceil(Nx/2) #Mid-point of x
mpy = ceil(Ny/2) #Mid point of y   
Ni = 11          #Number of iterations for the Poisson solver

h = 1.0/Nx       #changing top number creates a domain aspect ratio

T = 0            #Top-wall potential
B = 0            #Bottom-wall potential
L = 0            #Left-wall potential
R = 0            #Right-wall potential

V = [ [0.0] * Nx for _ in range(Ny) ]  #Potential (Voltage) matrix

for i in range(Nx):
    V[0][i] = L
    V[Nx-1][i] = R
    V[i][0] = B
    V[i][Ny-1] = T

V[0][0] = 0.5 * (V[0][1] + V[1][0])
V[Nx-1][0] = 0.5 * (V[Nx-2][0] + V[Nx - 1][2])
V[0][Ny-1] = 0.5 * (V[0][Ny-1] + V[1][Ny-1])
V[Nx - 1][Ny - 1] = 0.5 * (V[Nx-1][Ny-2] + V[Nx-2][Ny-1])

length_plate = ceil(Nx / 2.0)  #Length of plate in terms of number of grids  
lp = floor(length_plate / 2)

position_plate = ceil(Nx * 0.15) #Position of plate on x axis
pp1 = mpx + position_plate - 3
pp2 = mpx - position_plate

nt = 256
alpha = 0.0; dt = 0.0
capmat = [0.0] * nt; charge = [0.0] * nt; dCharge = [0.0] * nt; wmat = [0.0] * nt 

e0 = 8.854e-9; eR = 1.006
Er = [ [e0 * eR] * Nx for _ in range(Ny) ] 


Ex = [ [0.0] * Nx for _ in range(Ny) ]
Ey = [ [0.0] * Ny for _ in range(Ny) ]

Epx = [ [0.0] * Nx for _ in range(Ny) ]
Epy = [ [0.0] * Ny for _ in range(Ny) ]

E = [ [0.0] * Nx for _ in range(Ny) ]
rhoR = [ [0.0] * Nx for _ in range(Ny) ]


C = 0.0; dC = 0.0; cO = 0.0; qO = 0.0; wave = 0.0; 

for t in range(nt):
    
    wave = -sin(dt * 2.0 * pi * (172.265625)).real
    wmat[t] = wave
    alpha = wave
    dt = dt + (1/44100.0)
    
    C = 0.0
    
    for z in range(Ni):
        
        for x in range(1, Nx - 2):
            for y in range(1, Ny - 2):
                
                #boundary conditions
                for q in range(mpy - lp, mpy + lp):
                    V[pp1 + 1][q] = (alpha * 147)
                    V[pp1][q] = (1.0 - alpha) * 147
                    V[pp2][q] = 0
                  
                for q in range(1, Nx - 2):
                    for o in range(1, Ny - 2):
                        #five point stencil, solved for the central voltage
                        V[q][o] = (V[q - 1][o] + V[q][o - 1] + V[q + 1][o] + V[q][o + 1]) * 0.25

    V = matrixTranspose(V)

    [Ex , Ey] = np.gradient(V, h)

    e0 = 8.85e-12       
    for o in range(len(Ex)):
        for q in range(len(Ex[0])):

            Ex[o][q] *= -1.0 
            Ey[o][q] *= -1.0

            E[o][q] = sqrt( Ex[o][q]**2.0 + Ey[o][q]**2.0 ).real
            E[o][q] *= -e0

    iC = np.trapz(E)
    C = np.trapz(iC)

    charge[t] = C
    dC = (C - cO)/2.0
    cO = C

mplt.plot(charge)
mplt.show()