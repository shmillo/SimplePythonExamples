import numpy as np

def transpositionStringToInt(transposition):
    intToReturn = 0
    if(transposition == 'C'):
        intToReturn = 0
    elif(transposition == 'Db'):
        intToReturn = 1
    elif(transposition == 'D'):
        intToReturn = 2
    elif(transposition == 'Eb'):
        intToReturn = 3
    elif(transposition == 'E'):
        intToReturn = 4
    elif(transposition == 'F'):
        intToReturn = 5
    elif(transposition == 'Gb'):
        intToReturn = 6
    elif(transposition == 'G'):
        intToReturn = 7
    elif(transposition == 'Ab'):
        intToReturn = 8
    elif(transposition == 'A'):
        intToReturn = 9
    elif(transposition == 'Bb'):
        intToReturn = 10
    elif(transposition == 'B'):
        intToReturn = 11
    return intToReturn

def modePitchClass(modeString, transposition, octaveWrap):

    rootNote = 0
    if(isinstance(transposition, str)):
        rootNote = transpositionStringToInt(transposition)
    elif(isinstance(transposition, int)):
        rootNote = transposition

    modeLUT = []
    if(modeString == "major"):
        modeLUT = list([0, 2, 4, 5, 7, 9, 11])
    elif(modeString == "minor_n"):
        modeLUT = list([0, 2, 3, 5, 7, 8, 10])
    elif(modeString == "minor_h"):
        modeLUT = list([0, 2, 3, 5, 7, 8, 11])
    elif(modeString == "dorian"):
        modeLUT = list([0, 2, 3, 5, 7, 9, 10])
    elif(modeString == "phrygian"):
        modeLUT = list([0, 1, 3, 5, 6, 8, 10])
    elif(modeString == "phrygian_dom"):
        modeLUT = list([0, 1, 4, 5, 7, 9, 10])
    elif(modeString == "phrygian_maj"):
        modeLUT = list([0, 2, 4, 5, 6, 9, 10])
    elif(modeString == "mixolydian"):
        modeLUT = list([0, 2, 4, 5, 7, 9, 10])
    elif(modeString == "lydian"):
        modeLUT = list([0, 2, 4, 6, 7, 9, 10])
    elif(modeString == "aeolian"):
        modeLUT = list([0, 2, 3, 5, 7, 8, 10])
    elif(modeString == "locrian"):
        modeLUT = list([0, 1, 3, 4, 7, 9, 11])
    elif(modeString == "locrian_s"):
        modeLUT = list([0, 1, 3, 4, 6, 8, 10])
    
    modeLUT = np.array(modeLUT)
    modeLUT += rootNote
    if(octaveWrap):
        modeLUT %= 12
    return modeLUT


    
print(modePitchClass("major", "D", octaveWrap=1))


