def intToBinary(o):

    binaryNumber = [0.0] * 8
    
    binaryNumber[0] = (o&1)
    binaryNumber[1] = (o&2)>>1
    binaryNumber[2] = (o&4)>>2
    binaryNumber[3] = (o&8)>>3
    binaryNumber[4] = (o&16)>>4
    binaryNumber[5] = (o&32)>>5
    binaryNumber[6] = (o&64)>>6
    binaryNumber[7] = (o&128)>>7

    print(binaryNumber)

    return binaryNumber

def numberOfTrailingZeros(r):
    
    bit = intToBinary( int(r) )
    zero = 0
    for x in range( len(bit) ):

        if (bit[x] == 0):
            zero += 1  
        # if '1' comes then break
        else:
            break
 
    return zero

