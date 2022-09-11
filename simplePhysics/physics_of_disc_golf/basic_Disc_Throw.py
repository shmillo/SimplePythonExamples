from cmath import pi
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as mplt

#gravitational acceleration
g = -9.81; 

#mass
m = 0.155; 

#density of air
RHO = 1.23; 

#area
AREA = 0.05068; 

#lift
CLO = 0.01
#alpha lift
CLA = 1.0014
#drag
CDO = 0.08
#alpha drag
CDA = 2.72

ALPHAO = -4.0
#angle of throw in degrees,
alpha = 0.10001

#lift coeff
cl = CLO + CLA*alpha*pi/180.0
#drag coeff
cd = CDO + CDA*pow(alpha - ALPHAO*pi/180, 2.0)

#initial space positions
x = 0.0; yO = 1.0; y = yO; 
#initial velocities
vxO = 25.0; vx = vxO; 
vyO = 25.0; vy = vyO

xArr = []; yArr = []; timeArr = []
maxSteps = 12000; deltaT = 0.01; time = 0.0
for i in range(0, maxSteps):
    if( y > 0.0):
        #change in y velocity
        #derivation = net force set equal to grav force and lift force solved for dV/dT
        deltavy = (RHO*(vx**2.0)*AREA*cl/2.0/m+g)*deltaT
        #change in x velocity
        deltavx = -RHO*(vx**2.0)*AREA*cd*deltaT

        vx += deltavx; vy += deltavy
        x += vx*deltaT; y += vy*deltaT
        xArr.append(x); yArr.append(y); timeArr.append(time)
        time += deltaT

mplt.plot(xArr, yArr)
mplt.show()


