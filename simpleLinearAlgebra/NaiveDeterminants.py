

def det2x2(A):

    return A[0][0]*A[1][1] - A[0][1]*A[1][0]

def det3x3(A):

    partOne = A[0][0] * det2x2( [[ A[1][1], A[1][2] ], [ A[2][1], A[2][2] ]] )
    partTwo = -1.0 * A[0][1] * det2x2( [[ A[1][0], A[1][2] ], [ A[2][0], A[2][2] ]] )
    partThree = A[0][2] * det2x2( [[ A[1][0], A[1][1] ], [ A[2][0], A[2][1] ]] )

    return partOne + partTwo + partThree

def iterative3x3Det(A):

    cofactorArray = [0.0] * 3
    minorArray = [ [0.0] * 2 for _ in range( 2 ) ]

    scalar = 1.0
    for i in range(3):
        j = 0  
        for x in range(3):
            k = 0
            if( x != 0 ):
                for y in range(3):
                    if(y != i):
                        minorArray[j][k] = A[x][y]
                        k += 1
                j += 1

        cofactorArray[i] = scalar * A[0][i] * det2x2(minorArray)   
        scalar *= -1.0 
 
    determinant = 0.0
    for l in range( len(cofactorArray) ):
        determinant += cofactorArray[l]

    return determinant
        

def iterative4x4Det(A):

    cofactorArray = [0.0] * 4
    minorArray = [ [0.0] * 3 for _ in range( 3 ) ]

    scalar = 1.0
    for i in range(4):
        j = 0  
        for x in range(4):
            k = 0    
            if( x != 0 ):
                for y in range(4):
                    if(y != i):
                        minorArray[j][k] = A[x][y]
                        k += 1
                j += 1

        cofactorArray[i] = scalar * A[0][i] * iterative3x3Det(minorArray)   
        scalar *= -1.0 
 
    determinant = 0.0
    for l in range( len(cofactorArray) ):
        determinant += cofactorArray[l]

    return determinant                  

A = [ [0.0, 1.0], [4.0, 5.0] ]
print( det2x2(A) )

B = [ [9.0, 1.0, 2.0], [3.0, 4.0, 5.0], [6.0, 7.0, 8.0] ]
print( det3x3(B) )
print( iterative3x3Det(B) )

C = [ [11.0, 2.0, 3.0, 43.0], [51.0, 6.0, 7.0, 8.0], [9.0, 10.0, 11.0, 12.0], [13.0, 14.0, 15.0, 16.0] ]
print( iterative4x4Det(C) )