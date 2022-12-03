from PIL import Image
import numpy as np
import matplotlib.pyplot as mplt
from matplotlib.colors import LightSource
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.colors as mcolors

imageImport = Image.open("/Users/shawnmilloway/Desktop/Houdini_oil_v9_003.jpg")
imageImport = imageImport.convert("RGBA")
imageData = np.asarray(imageImport); print(np.shape(imageData))
attribs = []; attribs = np.shape(imageData)

size = 4; rowsX = int(attribs[0]/size); rowsY = int(attribs[1]/size); heightMap = np.zeros([rowsY, rowsY])
for i in range(rowsY):
    for j in range(rowsY):
        x = i * size; y = j * size
        red = imageData[x][y][0]/255
        green = imageData[x][y][1]/255
        blue = imageData[x][y][2]/255
        heightMap[i][j] = (((red + green + blue)/3.0) )

xAxis = np.linspace(-1.0, 1.0, num=rowsY); yAxis = np.linspace(-1.0, 1.0, num=rowsY); X, Y = np.meshgrid(xAxis, yAxis)

hX = X*(1.0 - (Y**2.0 * 0.5))**0.5; hY = Y*(1.0 - (X**2.0 * 0.5))**0.5

fig = mplt.figure(figsize=(10,10), dpi=900); fig.tight_layout(pad=0)
ax = fig.add_subplot(projection='3d'); ax.axis('off'); ax.set_xlim([-0.8, 0.8]); ax.set_ylim([-0.8, 0.8]) 
ax.azim = -48.0; ax.elev = 90; ax.dist = 5
ls = LightSource(attribs[0], attribs[1])
rgb = ls.shade(heightMap, cmap=mplt.cm.gist_earth, vert_exag=0.1, blend_mode='soft')
ax.scatter(hX, hY, heightMap, s=10.0*heightMap, c=heightMap, antialiased=False)
mplt.savefig('image_to_hyperbolic_plane_hi_dpi2.png')
mplt.show()