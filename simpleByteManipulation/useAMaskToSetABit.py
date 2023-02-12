def intToBinary(o):
    binaryNumber = [0.0] * 8
    binaryNumber[7] = (o&1)
    binaryNumber[6] = (o&2)>>1
    binaryNumber[5] = (o&4)>>2
    binaryNumber[4] = (o&8)>>3
    binaryNumber[3] = (o&16)>>4
    binaryNumber[2] = (o&32)>>5
    binaryNumber[1] = (o&64)>>6
    binaryNumber[0] = (o&128)>>7
    return binaryNumber

value = 0b00000000; valueMask = 0b00000001

result = (value | (valueMask << 0))

print(result, intToBinary(result))