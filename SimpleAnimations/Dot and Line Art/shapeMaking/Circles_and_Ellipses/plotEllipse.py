import numpy as np
import matplotlib.pyplot as mplt

nx = 100; ny = 100

arcHeight = ny * 0.1
arcBeginningPoint = nx * 0.1; arcEndingPoint = nx * 0.9
arcLengthInGridPoints = int(arcEndingPoint - arcBeginningPoint)
arcWidth = arcLengthInGridPoints//2

arcGeneratorPoints = np.linspace(0, 360, arcLengthInGridPoints) * (np.pi/180.0)
arcGeneratorPoints = arcGeneratorPoints[arcGeneratorPoints >= 0.0]

arcPointsX = arcWidth * np.cos(arcGeneratorPoints); 
arcPointsY = arcHeight * np.sin(arcGeneratorPoints)

arcXPoints = np.arange(arcBeginningPoint, arcEndingPoint + 1, 1)



mplt.plot(arcPointsX, arcPointsY)
mplt.show()