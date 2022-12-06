import numpy as np
from PIL import Image
import matplotlib.pyplot as mplt

def convolutionUnsharpMask(imData):

    kernel = [-1.0, 4.0, 6.0, 4.0, 1.0, 4.0, 16.0, 24.0, 16.0, 4.0, 6.0, 24.0, -476.0, 24.0, 6.0, 4.0, 16.0, 24.0, 16.0, 4.0, 1.0, 4.0, 6.0, 4.0, 1.0]
    kernel = np.array(kernel); kernel *= -1.0/256.0 #; print(int((len(kernel)**0.5 - 1)/2))

    indexModifiers = []; value = int((len(kernel)**0.5 - 1)/2)
    for x in range(value, -value - 1, -1):
        for y in range(value, -value - 1, -1):
            indexModifiers.append([y, x])
    indexModifiers = np.array(indexModifiers)
    print(len(kernel), len(indexModifiers))

    convolved = np.zeros_like(imageData, dtype=np.int64)
    color = np.zeros(imData.shape[2], dtype=np.float32)

    for x in range(1, imData.shape[0] - indexModifiers.max()):
        for y in range(1, imData.shape[1] - indexModifiers.max()):  
            r,g,b,a = 0.0, 0.0, 0.0, 0.0
            for kIndex in range(len(kernel) - 1, 0, -1):
                xx = x + indexModifiers[kIndex][0]; yy = y + indexModifiers[kIndex][1]
                color = imData[xx][yy]
                k = kernel[kIndex]
                r += k * float(color[0]); g += k * float(color[1]); b += k * float(color[2]); a += k * float(color[3])
            convolved[x][y] = (int(r), int(g), int(b), int(a))
    return convolved

#/Users/shawnmilloway/Desktop/rutt_etra_self_prtrait_copy.png
imageImport = Image.open("/Users/shawnmilloway/Desktop/pic.png")
imageImport = imageImport.convert("RGBA")
imageData = np.asarray(imageImport); print(np.shape(imageData))

conv = convolutionUnsharpMask(imageData)
conv = convolutionUnsharpMask(conv)
print(conv)

fig = mplt.figure(figsize=(5, 5)); fig.tight_layout(pad=0); ax = fig.add_subplot(111)
ax.imshow(conv)
mplt.show()
