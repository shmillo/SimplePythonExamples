import numpy as np
import matplotlib.pyplot as mplt

def colorFromRadius(xData):
    return (xData.max()**2.0 - xData**2.0)

waveResolution = 5000; l = 100; w = 100; gridL = (2 * l+1); gridW = (2*w+1); hashGrid = np.zeros([gridL, gridW])
viewXAxis = [0.05*gridW, 0.95*gridW]; viewYAxis = [0.05*gridL, 0.95*gridL]

x = np.linspace(0, 360, num=waveResolution); x *= np.pi/180.0
y = np.copy(x); angleX = np.cos(x); angleY = np.sin(y); randomModifiers = np.random.rand(x.shape[0])
radius = 10.0; scaledRadius = (l/radius)
angleX *= scaledRadius; angleX += randomModifiers; angleY *= scaledRadius; angleY += randomModifiers

randomVelocities = 360 * np.random.rand(x.shape[0]); randomVelocities *= np.pi/180.0
radialVelocityX = np.cos(randomVelocities); radialVelocityY = np.sin(randomVelocities)

numberOfTimeSteps = 50; radialAcceleration = (l/10.0); minimumAcceleration = 0.1;  
deaccelerationIncrements = np.linspace(radialAcceleration, minimumAcceleration, num=numberOfTimeSteps) 
for i in range(numberOfTimeSteps):

    randomPerturbations = np.random.rand(x.shape[0]); randomPerturbations += 1.0

    angleX = angleX + radialAcceleration * (radialVelocityX * randomPerturbations)
    angleY = angleY + radialAcceleration * (radialVelocityY * randomPerturbations)
    if(radialAcceleration >= minimumAcceleration):
        radialAcceleration = deaccelerationIncrements[i]

    angleX = np.round(angleX).astype(np.int16); angleY = np.round(angleY).astype(np.int16)   
    angleX[angleX > l] = l - 1; angleY[angleY > w] = w - 1; angleX[angleX < -l] = -l; angleY[angleY < -w] = -w

    hashGrid.fill(0.0); hashGrid[angleX + l, angleY + w] = colorFromRadius(angleX)

    mplt.clf(); mplt.axis('off'); mplt.xlim(viewXAxis); mplt.ylim(viewYAxis)
    mplt.tight_layout(pad=0); mplt.imshow(hashGrid, cmap='seismic'); mplt.draw(); mplt.pause(0.0001)
    
mplt.show()