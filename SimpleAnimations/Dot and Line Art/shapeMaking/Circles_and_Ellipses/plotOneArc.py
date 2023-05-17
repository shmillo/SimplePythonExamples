import numpy as np
import matplotlib.pyplot as mplt

nx = 100; ny = 100

arcAngle = 180; arcHeight = ny * 0.1
arcBeginningPoint = nx * 0.2; arcEndingPoint = nx * 0.8
arcLengthInGridPoints = arcEndingPoint - arcBeginningPoint; step = 2.0/arcLengthInGridPoints

arcGeneratorPoints = np.arange(-1.0, 1.0 + step, step)
arcPoints = arcHeight - (arcHeight * arcGeneratorPoints**2.0)

arcXPoints = np.arange(arcBeginningPoint, arcEndingPoint + 1, 1)

mplt.plot(arcXPoints, arcPoints)
mplt.show()