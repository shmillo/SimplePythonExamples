def indexesOfDiatonicTriadsInAMode(romanNumeralRootOfChord):
    indexesToReturn = []
    if(romanNumeralRootOfChord == 1):
        indexesToReturn = list([0, 2, 4])
    elif(romanNumeralRootOfChord == 2):
        indexesToReturn = list([1, 3, 6])
    elif(romanNumeralRootOfChord == 3):
        indexesToReturn = list([2, 4, 7])
    elif(romanNumeralRootOfChord == 4):
        indexesToReturn = list([3, 6, 0])
    elif(romanNumeralRootOfChord == 5):
        indexesToReturn = list([4, 7, 1])
    elif(romanNumeralRootOfChord == 6):
        indexesToReturn = list([5, 0, 2])
    elif(romanNumeralRootOfChord == 7):
        indexesToReturn = list([6, 1, 3])

    return indexesToReturn

def diatonicSeventhChord(romanNumeralRootOfChord):
    indexesToReturn = indexesOfDiatonicTriadsInAMode(romanNumeralRootOfChord)
    if(romanNumeralRootOfChord == 1):
        indexesToReturn.append(6)
    elif(romanNumeralRootOfChord == 2):
        indexesToReturn.append(0)
    elif(romanNumeralRootOfChord == 3):
        indexesToReturn.append(1)
    elif(romanNumeralRootOfChord == 4):
        indexesToReturn.append(2)
    elif(romanNumeralRootOfChord == 5):
        indexesToReturn.append(3)
    elif(romanNumeralRootOfChord == 6):
        indexesToReturn.append(4)
    elif(romanNumeralRootOfChord == 7):
        indexesToReturn.append(5)

    return indexesToReturn   