import numpy as np
import matplotlib.pyplot as mplt

def intToBinary(o):
    binaryNumber = [0.0] * 8
    binaryNumber[7] = (o&1)
    binaryNumber[6] = (o&2)>>1
    binaryNumber[5] = (o&4)>>2
    binaryNumber[4] = (o&8)>>3
    binaryNumber[3] = (o&16)>>4
    binaryNumber[2] = (o&32)>>5
    binaryNumber[1] = (o&64)>>6
    binaryNumber[0] = (o&128)>>7
    return binaryNumber

def multiplySquareMatrices(A, B):
    C = np.zeros_like(A, dtype=np.float32)
    m = A.shape[0]; r = B.shape[0]; n = B.shape[1]
    for i in range(0, m, 1):
        for j in range(0, r, 1):
            for k in range(0, n, 1): 
                C[i][j] += A[i][k] * B[k][j]
    return C

rotationMatrix = [
                    [0, 0, 0, 0, 0, 0, 0, 0], 
                    [1, 0, 0, 0, 0, 0, 0, 0], 
                    [0, 1, 0, 0, 0, 0, 0, 0], 
                    [0, 0, 1, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 1, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 1, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0]
                                                ]
rotationMatrix = np.array(rotationMatrix, dtype=np.float32)

fig, ax = mplt.subplots(1); ax.set_xlim([0, 8]); ax.set_ylim([0, 8])
xAxis = np.arange(0, 8, 1); yAxis = np.arange(0, 8, 1); X, Y = np.meshgrid(xAxis, yAxis)

valueMask = 0b00000111; ruleMask = 0b00000001; writeMask = 0b00000001
value = 0b00010000; rule = 0b00011010; tempValue = 0b00001000

plotArrays = np.zeros([8, 8]); numberOfGenerations = 100
for i in range(numberOfGenerations):
    tempValue = value
    for n in range(6):
        ruleIdx = (value & (valueMask<<n))>>n
        ruleBit = (rule & (ruleMask << ruleIdx))>>(ruleIdx)
        tempValue = (tempValue & ~(writeMask<<n+1)) | (ruleBit<<n+1)
    value = tempValue

    plotArrays = multiplySquareMatrices(rotationMatrix, plotArrays)
    plotArrays[0] = intToBinary(value)
    
    ax.scatter(X, Y, 100 * plotArrays)
    mplt.draw()
    mplt.pause(0.5)
    mplt.cla()

