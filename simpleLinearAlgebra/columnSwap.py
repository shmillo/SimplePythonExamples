
def matrixMultiply(A, B):

    n = len(A)
    m = len(B[0])

    C = [ [0.0] * m for _ in range(n) ]

    for i in range(n):
        for j in range(m):
            for k in range(len(A[0])):
                C[i][j] += A[i][k] * B[k][j]

    return C
            
def columnSwap(A, r1, r2):

    E = [ [0.0] * len(A[0]) for _ in range(len(A)) ]

    E[r1][r2] = 1.0
    E[r2][r1] = 1.0

    for i in range(len(A)):
        for j in range(len(A[0])):

            if(i != r1 and j != r1):
                if(i != r2 and j != r2):

                    if(i == j):
                        E[i][j] = 1.0

    return matrixMultiply(A, E)

testMatrix = [ [0,1],[2,3],[4,5] ]

result = columnSwap(testMatrix, 0,1)
print(result)