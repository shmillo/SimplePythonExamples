import numpy as np
import matplotlib.pyplot as mplt
from PIL import Image

#/Users/shawnmilloway/Desktop/pic.png
imageImport = Image.open("/Users/shawnmilloway/Desktop/Hand_Model.jpeg")
imageImport = imageImport.convert("RGBA")
imageData = np.asarray(imageImport); print(np.shape(imageData))
attribs = []; attribs = np.shape(imageData)

size = 2; rowsX = int(attribs[0]/size); rowsY = int(attribs[1]/size); heightMap = np.zeros([rowsY, rowsY])
for i in range(rowsY):
    for j in range(rowsY):
        x = i * size; y = j * size
        red = imageData[x][y][0]/255
        green = imageData[x][y][1]/255
        blue = imageData[x][y][2]/255
        heightMap[i][j] = (255 * ((red + green + blue)/3.0) )

x = np.linspace(0, rowsY, rowsY); y = np.linspace(0, rowsY, rowsY); X, Y = np.meshgrid(x, y)
print(np.shape(X), np.shape(Y), np.shape(heightMap))

fig = mplt.figure(figsize=(5, 5)); fig.tight_layout(pad=0); ax = fig.add_subplot(111, projection='3d'); ax.axis('off')
ax.dist = 6; ax.azim = 0.0; ax.elev = -84
surf = ax.plot_wireframe(X, Y, heightMap, rstride=0, cstride = 20,  linewidth=1)
mplt.show()
