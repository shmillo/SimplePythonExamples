def vectorTranspose(A):

    rowsInA = len( A )
    print(rowsInA)

    B = [ [0.0] * 1 for _ in range( rowsInA ) ]
    print(B)

    for i in range( rowsInA ):

        B[i][0] = A[i]
        
    return B


rows = 5

A = [ 1.0, 2.0, 3.0, 4.0, 5.0 ]

print( vectorTranspose(A) )
print( A )