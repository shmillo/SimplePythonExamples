import numpy as np

def powerIteration(A, numIts):

    b_k = np.random.rand(A.shape[1])

    for _ in range(numIts):
        bk1 = np.dot(A, b_k)
        bk1Norm = np.sqrt(sum(bk1**2.0))
        bk = bk1 / bk1Norm

    return bk

print( powerIteration(np.array([[0.5, 0.5], [0.2, 0.8]]), 10) ) 