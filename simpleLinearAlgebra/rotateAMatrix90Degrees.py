import numpy as np

def rotate90(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0])-1,-1,-1)]

def rotate90Alternate(mat):
    N = mat.shape[0]
    for x in range(N // 2):
        for y in range(x, N - x - 1):
            temp = mat[x][y]
            mat[x][y] = mat[y][N - 1 - x]
            mat[y][N - 1 - x] = mat[N - 1 - x][N - 1 - y]
            mat[N - 1 - x][N - 1 - y] = mat[N - 1 - y][x]
            mat[N - 1 - y][x] = temp
    return mat

valueArrays = np.zeros([8,8], dtype=np.int8)
valueArrays[:valueArrays.shape[0]//2, 3] = 1
print(valueArrays)

for i in range(4):
    valueArrays = rotate90(valueArrays)
    print(valueArrays)