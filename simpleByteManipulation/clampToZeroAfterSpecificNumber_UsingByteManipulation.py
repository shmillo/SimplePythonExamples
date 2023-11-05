
valToCheck = 0; numberAfterWhichValuesBecomeZero = 7; checkTempValue = numberAfterWhichValuesBecomeZero + 1
for i in range(15):
  valToCheck += 1
  print( (checkTempValue ^ (( valToCheck ^ checkTempValue ) & -( valToCheck < checkTempValue ))) & numberAfterWhichValuesBecomeZero ) 