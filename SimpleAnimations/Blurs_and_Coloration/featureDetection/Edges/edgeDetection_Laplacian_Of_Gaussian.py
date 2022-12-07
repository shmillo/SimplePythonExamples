import numpy as np
import math
from PIL import Image
import matplotlib.pyplot as plt

###########################################################################
###########################################################################

def grayConversion(image):
    height, width, channel = image.shape
    for i in range(0, height):
        for j in range(0, width):
            blueComponent = image[i][j][0]
            greenComponent = image[i][j][1]
            redComponent = image[i][j][2]
            grayValue = 0.07 * blueComponent + 0.72 * greenComponent + 0.21 * redComponent
            image[i][j] = (grayValue, grayValue, grayValue, image[i][j][3])
    return image

###########################################################################
###########################################################################

def logElement(x, y, theta):
    g = 0
    for ySubPixel in np.arange(y - 0.5, y + 0.55 + 0.1, 0.1):
        for xSubPixel in np.arange(x - 0.5, x + 0.55 + 0.1, 0.1):
            s = -((xSubPixel*xSubPixel)+(ySubPixel*ySubPixel))/(2*theta*theta)
            g = g + (1/(np.pi*(theta**4)))*(1+s)*np.exp(s)
    g = -g/121
    return g

def generateLOGKernel(kernelSize, theta):
    logKernel = np.zeros([kernelSize, kernelSize])
    for j in range(kernelSize):
        for i in range(kernelSize):
            x = (-kernelSize/2)+i
            y = (-kernelSize/2)+j
            logKernel[i][j] = logElement(x,y, theta)
    return logKernel

###########################################################################
###########################################################################

def laplacianOfGaussian(sigma, x, y):
    laplace = -1/(np.pi*sigma**4)*(1-(x**2+y**2)/(2*sigma**2))*np.exp(-(x**2+y**2)/(2*sigma**2))
    return laplace

def LogDiscrete(sigma, n):
    l = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            l[i,j] = laplacianOfGaussian(sigma, (i-(n-1)/2),(j-(n-1)/2))
    return l

###########################################################################
###########################################################################

def twoDimensionalConvolution(imData, kernel):

    indexModifiers = []; value = math.ceil((len(kernel)**0.5 - 1)/2)
    for x in range(value, -value - 1, -1):
        for y in range(value, -value - 1, -1):
            indexModifiers.append([y, x])
    indexModifiers = np.array(indexModifiers) 

    convolved = np.zeros_like(imData, dtype=np.int64)
    color = np.zeros(imData.shape[2], dtype=np.float32)

    for x in range(imData.shape[0]):
        for y in range(imData.shape[1]):  
            r, g, b, a = 0.0, 0.0, 0.0, 0.0
            for kIndex in range(len(kernel) - 1, 0, -1):
                color = 0.0
                xx = x + indexModifiers[kIndex][0]; yy = y + indexModifiers[kIndex][1]
                if(xx >= 0 and yy >= 0 and xx < imData.shape[0] and yy < imData.shape[1]):
                  color = imData[xx][yy]
                  k = kernel[kIndex]
                  r += k * float(color[0]); g += k * float(color[1]); b += k * float(color[2]); a += k * float(color[3])
            convolved[x][y] = (int(r), int(g), int(b), int(a))
    return convolved

###########################################################################
###########################################################################

def normalize(values, lowerDes, upperDes, lowerAct, upperAct):
    return [lowerDes + (x - lowerAct) * (upperDes - lowerDes) / (upperAct - lowerAct) for x in values]

###########################################################################
###########################################################################

sigma = 0.7; kSize = 6
lgK = generateLOGKernel(kSize, sigma)
kSum = 0.0
for i in range(lgK.shape[0]):
    kSum += sum(lgK[i]) 
if(kSum != 0.0):
    delta = kSum/(kSize**2.0)
    for j in range(kSize):
        for i in range(kSize):
           lgK[i][j] = lgK[i][j] - delta
kernelColumn = lgK
kernelColumn = kernelColumn.reshape(-1)
print(kernelColumn.shape[0], sum(kernelColumn), kernelColumn)

###########################################################################

#/Users/shawnmilloway/Desktop/130546838_10225166369855121_5630650196599505556_n.jpeg
#/Users/shawnmilloway/Desktop/pic.png
imageImport = Image.open("/Users/shawnmilloway/Desktop/pic.png")
imageImport = imageImport.convert("RGBA")
imageData = np.asarray(imageImport)#; print(np.shape(imageData))

###########################################################################

outputImg = twoDimensionalConvolution(imageData, kernelColumn)
outputImg = np.round(np.array(normalize(outputImg, 0, 255, outputImg.min(), outputImg.max()), dtype=np.uint8))
#print(outputImg)

###########################################################################

fig, (ax4) = plt.subplots(1, figsize=(5,5), dpi=200)
ax4.imshow(outputImg)
plt.show()