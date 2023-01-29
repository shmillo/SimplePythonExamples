import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

def convolution_h(imData):
    global hashGrid

    kernel = [1.0/16.0, 4.0/16.0, 6.0/16.0, 4.0/16.0, 1.0/16.0]; kernel_half = 2
    convolved = np.zeros_like(hashGrid, dtype=np.float32)
    color = np.zeros(imData.shape[2])

    for y in range(0, imData.shape[1]):
        for x in range(0, imData.shape[0]):
            r, g, b, a = 0, 0, 0, 0
            for kernel_offset in range(-kernel_half, kernel_half + 1):
                try:
                    xx = x + kernel_offset
                    k = kernel[kernel_offset + kernel_half]
                    color = imData[xx][y]
                    r += color[0] * k; g += color[1] * k; b += color[2] * k; a += color[3] * k
                except IndexError:
                    k = kernel[kernel_offset + kernel_half]
                    r += 0.5 * k; g += 0.5 * k; b += 0.5 * k; a += 0.5 * k
            convolved[x][y] = (r, g, b, a)
    return convolved

def convolution_y(imData):
    global hashGrid

    kernel = [1.0/16.0, 4.0/16.0, 6.0/16.0, 4.0/16.0, 1.0/16.0]; kernel_half = 2
    convolved = np.zeros_like(hashGrid, dtype=np.float32)
    color = np.zeros(imData.shape[2])

    for y in range(0, imData.shape[1]):
        for x in range(0, imData.shape[0]):
            r, g, b, a = 0, 0, 0, 0
            for kernel_offset in range(-kernel_half, kernel_half + 1):
                try:
                    yy = y + kernel_offset
                    k = kernel[kernel_offset + kernel_half]
                    color = imData[x][yy]
                    r += color[0] * k; g += color[1] * k; b += color[2] * k; a += color[3] * k
                except IndexError:
                    k = kernel[kernel_offset + kernel_half]
                    r += 0.5 * k; g += 0.5 * k; b += 0.5 * k; a += 0.5 * k
            convolved[x][y] = (r, g, b, a)
    return convolved

def colorFromRadius(xData, radius):
    return (radius - xData**2.0)

def animFunc(i):
    global crestAngleX, crestAngleY, radialAcceleration, radialCrestVelocityX, radialCrestVelocityY, angleX, angleY, deaccelerationIncrements, hashGrid

    randomPerturbations = np.random.rand(x.shape[0]); randomPerturbations += 0.3
   
    crestAngleX = crestAngleX + (0.3 * radialAcceleration * radialCrestVelocityX)
    crestAngleY = crestAngleY + (0.3 * radialAcceleration * radialCrestVelocityY)

    angleX = angleX + (0.3 * (radialAcceleration * radialVelocityX) * randomPerturbations)
    angleY = angleY + (0.3 * (radialAcceleration * radialVelocityY) * randomPerturbations)

    radialAcceleration = deaccelerationIncrements[i]

    crestAngleX = np.round(crestAngleX).astype(np.int16); crestAngleY = np.round(crestAngleY).astype(np.int16)   
    crestAngleX[crestAngleX > l] = l - 1; crestAngleY[crestAngleY > w] = w - 1
    crestAngleX[crestAngleX < -l] = -l; crestAngleY[crestAngleY < -w] = -w

    angleX = np.round(angleX).astype(np.int16); angleY = np.round(angleY).astype(np.int16)   
    angleX[angleX > l] = l - 1; angleY[angleY > w] = w - 1
    angleX[angleX < -l] = -l; angleY[angleY < -w] = -w

    hashGrid.fill(0.0)
    hashGrid[angleX + l, angleY + w] = colorOne
    hashGrid[crestAngleX + l, crestAngleY + w] = colorTwo

    hashGrid = convolution_y(convolution_h(hashGrid))
    #hashGrid = convolution_y(convolution_h(hashGrid))

    hashGrid[angleX + l, angleY + w] = [0.0, 1.0, 0.5, 0.3]
    hashGrid[crestAngleX + l, crestAngleY + w] = colorTwo

    mplt.clf(); mplt.axis('off'); mplt.xlim(viewXAxis); mplt.ylim(viewYAxis)
    mplt.tight_layout(pad=0); mplt.imshow(hashGrid, interpolation='gaussian')
    
waveResolution = 5000; l = 500; w = 500; gridL = (2 * (l+1)); gridW = (2 * (w+1)); hashGrid = np.zeros([gridL, gridW, 4])
viewXAxis = [0.05*gridW, 0.95*gridW]; viewYAxis = [0.05*gridL, 0.95*gridL]

x = np.linspace(0, 360, num=waveResolution); x *= np.pi/180.0; 
y = np.copy(x); angleX = np.cos(x); angleY = np.sin(y)

radius = 10.0; scaledRadius = (l/radius); 

crestAngleX = np.linspace(0, 360, num=waveResolution*2); crestAngleX *= np.pi/180.0; crestAngleY = np.copy(crestAngleX); 
crestAngleX = np.cos(crestAngleX); crestAngleY = np.sin(crestAngleY)
crestAngleX *= scaledRadius; crestAngleY *= scaledRadius

randomCrestVelocities = 360.0 * np.random.rand(crestAngleX.shape[0]); randomCrestVelocities *= np.pi/180.0
radialCrestVelocityX = np.cos(randomCrestVelocities); radialCrestVelocityY = np.sin(randomCrestVelocities)

randomModifiers = np.random.rand(x.shape[0])
angleX *= scaledRadius; angleX += randomModifiers
angleY *= scaledRadius; angleY += randomModifiers

randomVelocities = np.linspace(0, 360, num=x.shape[0]) + (10.0 * np.random.rand(x.shape[0]))
randomVelocities = np.clip(randomVelocities, 0.0, 360.0); randomVelocities *= np.pi/180.0
radialVelocityX = np.cos(randomVelocities); radialVelocityY = np.sin(randomVelocities)

colorOne = [0.0, 1.0, 0.5, 1.0]; colorTwo = [1.0, 0.0, 0.5, 1.0]

numberOfTimeSteps = 50; radialAcceleration = (l/10.0); minimumAcceleration = 0.1;  
deaccelerationIncrements = np.linspace(radialAcceleration, minimumAcceleration, num=numberOfTimeSteps) 

fig = mplt.figure()
anim = FuncAnimation(fig, func=animFunc, frames=range(numberOfTimeSteps), interval=1)
#anim.save("shockwaveAlternate3.gif", fps=30)
mplt.show()