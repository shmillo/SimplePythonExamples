import numpy as np

def multiplySquareMatrices(A, B):
    C = np.zeros_like(A, dtype=np.float32)
    m = A.shape[0]; r = B.shape[0]; n = B.shape[1]
    for i in range(0, m, 1):
        for j in range(0, r, 1):
            for k in range(0, n, 1): 
                C[i][j] += A[i][k] * B[k][j]
    return C

rotationMatrix = [[0, 1], [1, 0]]
rotationMatrix = np.array(rotationMatrix)

testMatrix = np.random.rand(2,2); print(testMatrix)
rotatedRowsMatrix = multiplySquareMatrices(rotationMatrix, testMatrix); print(rotatedRowsMatrix)
rotatedColumnsMatrix = multiplySquareMatrices(testMatrix, rotationMatrix); print(rotatedColumnsMatrix)