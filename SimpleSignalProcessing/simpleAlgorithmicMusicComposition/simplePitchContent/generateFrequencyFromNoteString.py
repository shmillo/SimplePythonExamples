import numpy as np

def noteFrequenciesA440(note, octave):
    global noteArray

    noteTemp = note; octaveTemp = octave
    if(isinstance(note, str)):
        noteTemp = transpositionStringToInt(note)
    if(noteTemp >= 12):
        noteTemp %= 12
        octaveTemp += 1
    
    frequencyToReturn = 0.0
    if(octave < 9 and octave >= 0):
       frequencyToReturn = noteArray[octaveTemp][noteTemp]
    elif(octaveTemp < 0):
        frequencyToReturn = noteArray[0][noteTemp]
    elif(octaveTemp >= 9):
        frequencyToReturn = noteArray[9][noteTemp]

    return frequencyToReturn

noteArray = []
#C0 - B0
zeroOctave = [16.35, 17.32, 18.35, 19.45, 20.60, 21.83, 23.12, 24.50, 25.96, 27.50, 29.14, 30.87]
noteArray.append(zeroOctave)
#C1 - B1
oneOctave = [32.70, 34.65, 36.71, 38.89, 41.20, 43.65, 46.25, 49.00, 51.91, 55.0, 58.27, 61.74]
noteArray.append(oneOctave)
#C2 - B2
twoOctave = [65.41, 69.30, 73.42, 77.78, 82.41, 87.31, 92.50, 98.00, 103.83, 110.00, 116.54, 123.47]
noteArray.append(twoOctave)
#C3 - B3
threeOctave = [130.81, 138.59, 146.83, 155.56, 164.81, 174.61, 185.00, 196.00, 207.65, 220.00, 233.08, 246.94]
noteArray.append(threeOctave)
#C4 - B4
fourOctave = [261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88]
noteArray.append(fourOctave)
#C5 - B5
fiveOctave = [523.25, 554.37, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61, 880.00, 932.33, 987.77]
noteArray.append(fiveOctave)
#C6 - B6
sixOctave = [1046.50, 1108.73, 1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98, 1661.22, 1760.0, 1864.66, 1975.53]
noteArray.append(sixOctave)
#C7 - B7
sevenOctave = [2093.00, 2217.46, 2349.32, 2489.02, 2637.02, 2793.83, 2959.96, 3135.96, 3322.44, 3520.00, 3729.31, 3951.07]
noteArray.append(sevenOctave)
#C8 - B8
eightOctave = [4186.01, 4434.92, 4698.63, 4978.03, 5247.04, 5587.65, 5919.91, 6271.93, 6644.88, 7040.00, 7458.62, 7902.13]
noteArray.append(eightOctave)

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

#A440 but from pc-representation of 3rd octave
print(noteFrequenciesA440(21, 3))