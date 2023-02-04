import numpy as np
import matplotlib.pyplot as mplt

resolution = 2000; l = 1000; w = 1000; gridL = 1 + (l * 2); gridW = 1 + (w * 2)
hashGrid = np.zeros([gridL, gridW, 4], dtype=np.float32); grid = np.linspace(0, gridL, gridL).astype(np.int32)

rateInc = 0.0
gradient = np.zeros([gridL, gridW])
rateInc = rateInc + (2.0/(float(gradient.shape[0])))
for i in range(gridL//2):
    for y in range(i, gridW - i):
        gradient[i][y] = rateInc
        gradient[gridL - 1 - i][y] = rateInc
        gradient[y][gridL - 1 - i] = rateInc
        gradient[y][i] = rateInc
    rateInc = rateInc + (2.0/(float(gradient.shape[0])))

print( gradient.min(), gradient.max() )

rateInc = 1.0 
reverseGradient = np.zeros([gridL, gridW]); 
for i in range(gridL//2):
    for y in range(i, gridW - i):
        reverseGradient[i][y] = rateInc
        reverseGradient[gridL - 1 - i][y] = rateInc
        reverseGradient[y][gridL - 1 - i] = rateInc
        reverseGradient[y][i] = rateInc
    rateInc = rateInc - (2.0/(float(reverseGradient.shape[0])))

print( reverseGradient.min(), reverseGradient.max() )

hashGrid[:, :, 0] = gradient; hashGrid[:, :, 1] = gradient
hashGrid[:, :, 2] = gradient; hashGrid[:, :, 3] = 1.0

mplt.imshow(hashGrid)
mplt.show()

