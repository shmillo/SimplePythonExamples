def lmBit(x):
    #more | statements and longer LUT needed for higher bit counters
    bval = [ 0,1,2,2,3,3,3,3,4,4,4,4,4,4,4,4 ]
    result = (4*((x & 0x000000F0) > 1)) | ((x & 0x0000000F) > 1)
    return result + bval[ x >> result ]

valToCheck = 0; brightness = 10
for i in range(255):
  print(lmBit(valToCheck), bin(valToCheck))
  valToCheck += 1
