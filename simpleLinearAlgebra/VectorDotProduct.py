def dotProduct(A, B):

    c = 0.0

    for i in range( len(A) ):

        c += A[i] * B[i]

    return c

A = [0.0, 1.0, 2.0, 3.0]
B = [4.0, 5.0, 6.0, 7.0]

print( dotProduct(A,B) )

