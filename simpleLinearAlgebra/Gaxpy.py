def gaxpy(A,B):

    rowsInA = len( A )
    colsInA = len( A[0] )

    rowsInB = len( B )

    C = [0.0] * rowsInB  

    for i in range( rowsInB ):
        for j in  range( colsInA ):

            C[i] +=  A[i][j] * B[j]


rows = 5
columns = 5

A = [ [0.0] * rows for _ in range(columns) ]
B = [0.0] * columns 