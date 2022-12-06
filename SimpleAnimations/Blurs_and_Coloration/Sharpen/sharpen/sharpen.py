import numpy as np
from PIL import Image
import matplotlib.pyplot as mplt

def convolutionSharpen(imData):

    kernel = [0.0, -1.0, 0.0, -1.0, 5.0, -1.0, 0.0, -1.0, 0.0]
    indexModifiersMiddle = [[1,1], [0,1], [-1,1], [1,0], [0,0], [-1,0], [1,-1], [0,-1], [-1,-1]]

    convolved = np.zeros_like(imageData, dtype=np.int64)
    color = np.zeros(imData.shape[2], dtype=np.float32)

    for x in range(1, imData.shape[0] - 1):
        for y in range(1, imData.shape[1] - 1):  
            r,g,b,a = 0.0, 0.0, 0.0, 0.0
            for kIndex in range(len(kernel) - 1, 0, -1):
                xx = x + indexModifiersMiddle[kIndex][0]; yy = y + indexModifiersMiddle[kIndex][1]
                color = imData[xx][yy]
                k = kernel[kIndex]
                r += k * float(color[0]); g += k * float(color[1]); b += k * float(color[2]); a += k * float(color[3])
            convolved[x][y] = (int(r), int(g), int(b), int(a))
    return convolved


#/Users/shawnmilloway/Desktop/rutt_etra_self_prtrait_copy.png
imageImport = Image.open("/Users/shawnmilloway/Desktop/rutt_etra_self_prtrait_copy.png")
imageImport = imageImport.convert("RGBA")
imageData = np.asarray(imageImport); print(np.shape(imageData))

conv = convolutionSharpen(imageData)

fig = mplt.figure(figsize=(5, 5)); fig.tight_layout(pad=0); ax = fig.add_subplot(111)
ax.imshow(conv)
mplt.show()
