import numpy as np
import matplotlib.pyplot as mplt
import matplotlib as mpl
from matplotlib.animation import FuncAnimation

def exponentialEnvelope(x):
    return np.exp(-3.0 * x )

def animFunc(i):
    global cmap, time, signalX, signalY, numSegments, angleOfRotation, rotationRate, rotationRateMax, colorModulus, rotationRateGoal, negativeSpaceMask, angleAcceleration

    hashGrid.fill(0); 
    
    signalXTemp = np.roll(signalX, time); signalYTemp = np.roll(signalY, time)
    time = (time + 500) % signalX.shape[0]

    for segment in range(1, numSegments + 1):

        signalXTemp = np.roll(signalX, time); signalYTemp = np.roll(signalY, time); time = (time + 100) % signalXTemp.shape[0]

        angleOfRotation = rotationRate[segment - 1]
        cosScalar = np.cos(angleOfRotation); sinScalar = np.sin(angleOfRotation)

        currentRadius = segment/numSegments; radius = int(spatialResolution * currentRadius)
        outputX = angleX*radius; outputY = angleY*radius
        
        xTemp = ((cosScalar*outputX) - (sinScalar*outputY)) + (200.0 * (segment/numSegments) * signalXTemp) 
        yTemp = ((cosScalar*outputY) + (sinScalar*outputX)) + (200.0 * (segment/numSegments) * signalYTemp)

        x = np.array( np.round(xTemp), dtype=np.int32 ); y = np.array( np.round(yTemp), dtype=np.int32 )
        x[x > spatialResolution] = spatialResolution - 1; y[y > spatialResolution] = spatialResolution - 1

        hashGrid[x+spatialResolution, y+spatialResolution] = colorModulus
        
        colorModulus += 0.5/256.0
        if(colorModulus >= 1.0):
            colorModulus = 0

    if( rotationRateGoal == rotationRateMax and rotationRate.max() < rotationRateGoal ):
        rotationRate += angleAcceleration
        angleAcceleration += 0.0001
        if(rotationRate.max() >= rotationRateGoal):
            rotationRateGoal = 0.0
    elif( rotationRateGoal == 0.0 and rotationRate.max() > rotationRateGoal ):
        rotationRate -= angleAcceleration * 2.0
        if(rotationRate.min() <= rotationRateGoal):
            rotationRateGoal = rotationRateMax

    mplt.clf(); fig.set_facecolor('black'); ax.axis('off'); ax.set_facecolor('black')
    mplt.xlim([0.25*l, 0.75*l]); mplt.ylim([0.25*w, 0.75*w]); 
    mplt.imshow(hashGrid, cmap=cmap, interpolation='sinc')

fig, ax = mplt.subplots(1); fig.tight_layout(pad=0); fig.set_facecolor('black')
ax.axis('off'); ax.set_facecolor('black')
cmap = mpl.colors.ListedColormap(mplt.cm.hsv(np.linspace(0, 1, num=256)))

leftPoint = 0.0; rightPoint = 2.0
spatialResolution = 1000; l = int((rightPoint - leftPoint) * spatialResolution); w = int((rightPoint - leftPoint) * spatialResolution)
hashGrid = np.zeros([l + 1, w + 1]); negativeSpaceMask = np.ones_like(hashGrid)

numLines = 21; radians = np.linspace(0, 360, num=numLines)
x = []; x = np.array(x); lineThickness = 1000
for _ in range(2):
    for r in range(1, radians.shape[0], 2):
        startPoint = radians[r-1]; endPoint = radians[r]; spacing = (endPoint - startPoint)/lineThickness
        x = np.concatenate( (x, np.linspace(startPoint,  endPoint, num=lineThickness)) )
    x *= np.pi/180.0; 

y = np.copy(x); angleX = np.cos(x); angleY = np.sin(y)

numSegments = 1000
for segment in range(1, numSegments + 1):

  currentRadius = segment/numSegments; radius = int(spatialResolution * currentRadius)
  outputX = angleX*radius; outputY = angleY*radius

  x = np.array( np.round(outputX), dtype=np.int32 ); y = np.array( np.round(outputY), dtype=np.int32 )
  
  hashGrid[x+spatialResolution, y+spatialResolution] = 1.0

#mplt.xlim([0.25*l, 0.75*l]); mplt.ylim([0.25*w, 0.75*w])

angleOfRotation = 1.0; rotationRate = np.zeros(numSegments); rotationRateMax = 5000.0; rotationRateGoal = rotationRateMax; colorModulus = 0.0
angleAcceleration = (1.0/((np.array(range(1,numSegments+1)))))

time = 0

sampleRate = int((numLines-1)*numSegments); fundamentalHz = 2.0
periodInSeconds = 1.0/fundamentalHz; periodSamples = int(sampleRate*(periodInSeconds))
rippleTime = periodSamples; timeAxis = np.linspace(0.0, 1.0, int((numLines-1)*numSegments)); print(timeAxis)
envelope = np.zeros_like(timeAxis, dtype=np.float32); envelope[:rippleTime] = exponentialEnvelope(timeAxis[:rippleTime])
frequency = fundamentalHz/2.0; signal = np.zeros_like(timeAxis); signal[:rippleTime] = np.sin(2.0 * np.pi * frequency * timeAxis[:rippleTime]); 
signal = signal * envelope; signalX = np.cos(signal); signalY = np.sin(signal)

anim = FuncAnimation(fig, func=animFunc, frames=range(40), interval=1); anim.save('spiralRipples.gif', fps=30)
mplt.show()