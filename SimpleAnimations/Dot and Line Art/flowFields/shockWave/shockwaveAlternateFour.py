import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.animation import FuncAnimation

def perlin(x, y, seed=0):
    # permutation table
    np.random.seed(seed)
    p = np.arange(256, dtype=int)
    np.random.shuffle(p)
    p = np.stack([p, p]).flatten()
    # coordinates of the top-left
    xi, yi = x.astype(np.int32), y.astype(np.int32)
    # internal coordinates
    xf, yf = x - xi, y - yi
    # fade factors
    u, v = fade(xf), fade(yf)
    # noise components
    n00 = gradient(p[p[xi] + yi], xf, yf)
    n01 = gradient(p[p[xi] + yi + 1], xf, yf - 1)
    n11 = gradient(p[p[xi + 1] + yi + 1], xf - 1, yf - 1)
    n10 = gradient(p[p[xi + 1] + yi], xf - 1, yf)
    # combine noises
    x1 = lerp(n00, n10, u)
    x2 = lerp(n01, n11, u)  # FIX1: I was using n10 instead of n01
    return lerp(x1, x2, v)  # FIX2: I also had to reverse x1 and x2 here

def lerp(a, b, x):
    "linear interpolation"
    return a + x * (b - a)

def fade(t):
    "6t^5 - 15t^4 + 10t^3"
    return 6 * t**5 - 15 * t**4 + 10 * t**3

def gradient(h, x, y):
    "grad converts h to the right gradient vector and return the dot product with (x,y)"
    vectors = np.array([[0, 1], [0, -1], [1, 0], [-1, 0]])
    g = vectors[h % 4]
    return g[:, :, 0] * x + g[:, :, 1] * y

def animFunc(i):
    global frame, writeAmount, numberOfTimeSteps, xAngle, radius, displacementArrayX, displacementArrayY, l, w, hashGrid, radiusModifier

    print(frame); frame += 1

    xAngleTemp = np.round(xAngle*radius + displacementArrayX).astype(np.int32)
    yAngleTemp = np.round(yAngle*radius + displacementArrayY).astype(np.int32)
    xAngleTemp[xAngleTemp > l] = l; yAngleTemp[yAngleTemp > w] = w; 
    xAngleTemp[xAngleTemp < -l] = -l; yAngleTemp[yAngleTemp < -w] = -w

    distanceArr = np.sqrt( (xAngleTemp - radius)**2.0 + (yAngleTemp - radius)**2.0 )
    distanceArr /= 128.0; distanceArr[distanceArr > 1.0] = writeAmount; writeAmount *= 0.99
    
    hashGrid[hashGrid[:, :, 3] > 0.0] *= 0.918
    hashGrid[hashGrid[:, :, 2] > 0.0] *= 0.998
    hashGrid[hashGrid[:, :, 2] > 0.0] *= 0.918
    hashGrid[hashGrid[:, :, 0] > 0.0] *= 0.99

    #hashGrid.fill(0.0)
    hashGrid[xAngleTemp + l, yAngleTemp + w, 0] = 0.9
    hashGrid[xAngleTemp + l, yAngleTemp + w, 1] = distanceArr * 0.2
    hashGrid[xAngleTemp + l, yAngleTemp + w, 2] = distanceArr * 0.85
    hashGrid[xAngleTemp + l, yAngleTemp + w, 3] = distanceArr

    midSkew = 0.15
    midPointX = (midSkew * xAngleTemp.max()) + ((1.0 - midSkew) * xAngleTemp.min())
    distanceFromMidPoint = (xAngleTemp)**2.0 + (yAngleTemp)**2.0 - (midPointX**2.0)
    maskIdxX = xAngleTemp[distanceFromMidPoint > 0.0]; maskIdxY = yAngleTemp[distanceFromMidPoint > 0.0]

    shapeX = maskIdxX.shape[0]; shapeY = maskIdxY.shape[0]
    if(shapeX > shapeY):
        maskIdxX = maskIdxX[:shapeY]
    elif(shapeY > shapeX):
        maskIdxY = maskIdxY[:shapeX]
    
    midSkew = 0.95
    midPointXT = (midSkew * maskIdxX.max()) + ((1.0 - midSkew) * maskIdxX.min()); 
    midPointYT = (midSkew * maskIdxY.max()) + ((1.0 - midSkew) * maskIdxY.min()); 
    distanceFromMidMax = np.sqrt( (np.abs(maskIdxX) - midPointXT)**2.0 + (np.abs(maskIdxY) - midPointYT)**2.0 )
    distanceFromMidMax /= distanceFromMidMax.max()
    distanceFromMidMax = np.clip(distanceFromMidMax, 0.85, 1.0)

    hashGrid[maskIdxX + l, maskIdxY + w, 0] *= distanceFromMidMax
    hashGrid[maskIdxX + l, maskIdxY + w, 1] *= distanceFromMidMax
    hashGrid[maskIdxX + l, maskIdxY + w, 2] *= distanceFromMidMax
    hashGrid[maskIdxX + l, maskIdxY + w, 3] *= distanceFromMidMax

    radius = l/radiusModifier
    if(radiusModifier >= (0.5 + decInc)):
        radiusModifier -= decInc
    
    mplt.cla()
    mplt.xlim([0, gridL]); mplt.ylim([0, gridW]); mplt.axis('off'); mplt.tight_layout(pad=0)
    mplt.imshow(hashGrid)

resolution = 2000; l = 1000; w = 1000; gridL = 1 + (l * 2); gridW = 1 + (w * 2); hashGrid = np.zeros([gridL, gridW, 4], dtype=np.float32)

xAngle = np.linspace(0, 360, num=resolution); xAngle *= np.pi/180.0; yAngle = np.copy(xAngle)
xAngle = np.cos(xAngle); yAngle = np.sin(yAngle); 

lin = np.linspace(2, 15, resolution, endpoint=False); x, y = np.meshgrid(lin, lin)
radiusModifier = 5; radius = l/radiusModifier; maxDisplacement = (gridL - radius)//10 - 1
displacementArrayX = (xAngle * maxDisplacement * perlin(x, y))
displacementArrayY = (yAngle * maxDisplacement * perlin(x, y))

decInc = 0.1; numberOfTimeSteps = int( 10/decInc ); print(numberOfTimeSteps)
fig = mplt.figure(); frame = 0; writeAmount = 1.0
anim = FuncAnimation(fig, func=animFunc, frames=range(numberOfTimeSteps), interval=1)
anim.save("shockwaveT4.gif")
mplt.show()