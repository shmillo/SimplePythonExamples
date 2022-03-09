from cProfile import label
import matplotlib.pyplot as mplt

def KE(m, v):
    return 0.5 * m * v**2.0

def PE(m, g, p):
    return m * g * p

#Initialize 
velocity = 0.0
velocityArray = []

mass = 1.15

gravity = 9.8
acceleration = -1.0 * gravity

position = 200.0
positionArray = []

potentialEnergyArray = []
kineticEnergyArray = []
lagrangianArray = []

sampleRate = 10
dt = 1.0 / sampleRate
#simulation time needed is specific to gravity and initial position above 0.0
simulationTime = 7
numberOfTimeSteps = int( simulationTime * sampleRate )

for t in range( numberOfTimeSteps ):
   
   #integration of acceleration w.r.t time
    velocity += acceleration * dt
    velocityArray.append( velocity )

   #integration of velocity w.r.t time
    position += velocity * dt
    if( position < 0.0 ):
        #0.0 represents the ground, don't go through the ground
        position = 0.0
    positionArray.append( position )

    #kinetic and potential energy EQs derived from the lagrangian
    kineticEnergyArray.append( KE(mass, velocity) )
    potentialEnergyArray.append( PE(mass, gravity, position) )
    lagrangianArray.append( kineticEnergyArray[ t ] - potentialEnergyArray[ t ] )


fig, (ax1, ax2, ax3, ax4, ax5) = mplt.subplots( 5, sharex = True )

ax1.plot( velocityArray, label = 'velocity in m/s' )
ax1.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

ax2.plot( positionArray, label = 'position in m' )
ax2.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

ax3.plot( lagrangianArray, label = 'Lagrangian = KE - PE' )
ax3.legend( bbox_to_anchor = (0.0, 1), loc = 'upper left' )

ax4.plot( kineticEnergyArray, label = 'Kinetic Energy' )
ax4.legend( bbox_to_anchor = (0.0, 1), loc = 'upper left' )

ax5.plot( potentialEnergyArray, label = 'Potential Energy' )
ax5.legend( bbox_to_anchor = (1.0, 1), loc = 'upper right' )

mplt.show()