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

fig, (ax1, ax2) = plt.subplots(2)

grid = np.zeros([100,100]); tiling = 20; print(grid.shape)
n = int(grid.shape[0]/tiling); m = int(grid.shape[0]/tiling)
randPixels = np.random.random([n,m])
for i in range(grid.shape[0]):
  for j in range(grid.shape[0]):
    idxOne = math.floor(i/tiling); idxTwo = math.floor(j/tiling) #; print(j, idxOne, idxTwo)
    grid[i][j] = randPixels[idxOne][idxTwo]
print(grid.shape)

img = Image.fromarray(np.uint8(plt.cm.gist_earth(randPixels)*255))
rgbaArray = np.array(img.getdata(), np.uint8).reshape(img.size[1], img.size[0], 4)
ax1.imshow(rgbaArray, label='original image')

rgbaArray = grayConversion(rgbaArray)
ax2.imshow(rgbaArray, label='grayscale image')

plt.show()