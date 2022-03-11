import matplotlib.pyplot as mplt

def pointWiseMultiply( A, B ):

    rows = len( A )
    columns = len( A[0] )

    C = [ [0.0] * rows for _ in range(columns) ]

    for i in  range(rows):
        for j in range(columns):

            C[i][j]= A[i][j] * B[i][j]

    return C

def pointWiseDivide( A, B ):

    rows = len( A )
    columns = len( A[0] )

    C = [ [0.0] * rows for _ in range(columns) ]

    for i in  range(rows):
        for j in range(columns):

            if(B[i][j] != 0.0):
                C[i][j]= A[i][j] / B[i][j]

    return C


rows = 5
columns = 5

A = [ [0.0] * rows for _ in range(columns) ]
B = [ [0.0] * rows for _ in range(columns) ]

D = pointWiseMultiply(A, B)

print( D )