import numpy as np
import math
from PIL import Image
import matplotlib.pyplot as plt

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
   
def laplacianOfGaussian(sigma, x, y):
    laplace = -1/(np.pi*sigma**4)*(1-(x**2+y**2)/(2*sigma**2))*np.exp(-(x**2+y**2)/(2*sigma**2))
    return laplace

def LogDiscrete(sigma, n):
    l = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            l[i,j] = laplacianOfGaussian(sigma, (i-(n-1)/2),(j-(n-1)/2))
    return l

def twoDimensionalConvolution(imData, kernel):

    indexModifiers = []; value = int((len(kernel)**0.5 - 1)/2)
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

sigma = 1.4
kernelColumn = np.round(LogDiscrete(sigma, 9) * (-40/laplacianOfGaussian(sigma,0,0)))
kernelColumn = kernelColumn.reshape(-1); kernelColumn /= sum(kernelColumn)
print(kernelColumn.shape[0])

#/Users/shawnmilloway/Desktop/130546838_10225166369855121_5630650196599505556_n.jpeg
#/Users/shawnmilloway/Desktop/pic.png
imageImport = Image.open("/Users/shawnmilloway/Desktop/pic.png")
imageImport = imageImport.convert("RGBA")
imageData = np.asarray(imageImport); print(np.shape(imageData))

#rgbaArray = grayConversion(imageData)
#print(rgbaArray.shape)

outputImg = twoDimensionalConvolution(imageData, kernelColumn)
print(outputImg)

fig, (ax4) = plt.subplots(1, figsize=(5,5), dpi=200)
ax4.imshow(outputImg)
plt.show()