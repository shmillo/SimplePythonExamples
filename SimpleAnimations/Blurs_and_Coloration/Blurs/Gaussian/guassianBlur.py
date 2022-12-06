import numpy as np
from PIL import Image
import matplotlib.pyplot as mplt

def convolution_h(imData):

    kernel = [1.0/16.0, 4.0/16.0, 6.0/16.0, 4.0/16.0, 1.0/16.0]; kernel_half = 2
    convolved = np.zeros_like(imageData, dtype=np.int64)
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
                    r += 128 * k; g += 128 * k; b += 128 * k; a += 128 * k
            convolved[x][y] = (r, g, b, a)
    return convolved

def convolution_y(imData):

    kernel = [1.0/16.0, 4.0/16.0, 6.0/16.0, 4.0/16.0, 1.0/16.0]; kernel_half = 2
    convolved = np.zeros_like(imageData, dtype=np.int64)
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
                    r += 128 * k; g += 128 * k; b += 128 * k; a += 128 * k
            convolved[x][y] = (r, g, b, a)
    return convolved

#/Users/shawnmilloway/Desktop/rutt_etra_self_prtrait_copy.png
imageImport = Image.open("/Users/shawnmilloway/Desktop/rutt_etra_self_prtrait_copy.png")
imageImport = imageImport.convert("RGBA")
imageData = np.asarray(imageImport); print(np.shape(imageData))

conv = convolution_y(convolution_h(imageData)); print(conv)

fig = mplt.figure(figsize=(5, 5)); fig.tight_layout(pad=0); ax = fig.add_subplot(111)
#ax.dist = 5; ax.azim = -90.0; ax.elev = -92; ax.set_xlim([300, 1080])
ax.imshow(conv)
mplt.show()
