

def matrixTranspose(A):

    B = [ [A[j][i] for j in range(len(A))] for i in range(len(A[0])) ]
        
    return B

A = [ [1.0, 2.0, 3.0, 4.0, 5.0], [6.0, 7.0, 8.0, 9.0, 10.0] ]

print( matrixTranspose(A) )
print( A )