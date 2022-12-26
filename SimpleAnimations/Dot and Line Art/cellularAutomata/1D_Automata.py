import numpy as np
import matplotlib.pyplot as mplt

def nextGen(neighborL, Value, neighborR):
    global rule

    returnValue = 0
  
    if(neighborL == 1 and Value == 1 and neighborR == 1):
        returnValue = rule[7]
    elif(neighborL == 1 and Value == 1 and neighborR == 0):
        returnValue = rule[6]
    elif(neighborL == 1 and Value == 0 and neighborR == 1):
        returnValue = rule[5]
    elif(neighborL == 1 and Value == 0 and neighborR == 0):
        returnValue = rule[4]
    elif(neighborL == 0 and Value == 1 and neighborR == 1):
        returnValue = rule[3]
    elif(neighborL == 0 and Value == 1 and neighborR == 0):
        returnValue = rule[2]
    elif(neighborL == 0 and Value == 0 and neighborR == 1):
        returnValue = rule[1]
    elif(neighborL == 0 and Value == 0 and neighborR == 0):
        returnValue = rule[0]
  
    return returnValue

def intToBinary(o):

    binaryNumber = [0.0] * 8
    
    binaryNumber[0] = (o&1)
    binaryNumber[1] = (o&2)>>1
    binaryNumber[2] = (o&4)>>2
    binaryNumber[3] = (o&8)>>3
    binaryNumber[4] = (o&16)>>4
    binaryNumber[5] = (o&32)>>5
    binaryNumber[6] = (o&64)>>6
    binaryNumber[7] = (o&128)>>7

    print('rule =', binaryNumber)

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
generationSize = rotationMatrix.shape[0]

fig, ax = mplt.subplots(1); ax.set_xlim([0, generationSize]); ax.set_ylim([0, generationSize])
xAxis = np.arange(0, generationSize, 1); yAxis = np.arange(0, generationSize, 1); X, Y = np.meshgrid(xAxis, yAxis)

previousIteration = np.array([0, 1, 1, 0, 0, 1, 1, 0], dtype=np.float32); tempIteration = previousIteration; 
currentIteration = np.zeros_like(rotationMatrix, dtype=np.float32); currentIteration[0] = previousIteration

rule = intToBinary(37); rule = np.array(rule); numberOfIterations = generationSize * 5; size = 100 
for i in range(numberOfIterations):

    for j in range(1, previousIteration.shape[0] - 1):
        tempIteration[j] = nextGen(previousIteration[j - 1], previousIteration[j], previousIteration[j + 1])      
    previousIteration = tempIteration; print(previousIteration)
    
    currentIteration = multiplySquareMatrices(rotationMatrix, currentIteration)
    currentIteration[0] = previousIteration

    ax.scatter(X, Y, currentIteration*size)
    mplt.draw()
    mplt.pause(0.4)
    mplt.cla()

mplt.show()