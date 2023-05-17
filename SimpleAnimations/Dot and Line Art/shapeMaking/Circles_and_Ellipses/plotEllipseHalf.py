import numpy as np
import matplotlib.pyplot as mplt

nx = 100; ny = 100

arcHeight = 10.0
arcBeginningPoint = nx * 0.3; arcEndingPoint = nx * 0.9
arcLengthInGridPoints = int(arcEndingPoint - arcBeginningPoint)
arcWidth = arcLengthInGridPoints

arcGeneratorPoints = np.linspace(-arcWidth, arcWidth, arcLengthInGridPoints)

arcPoints = arcHeight * (1.0 - (arcGeneratorPoints**2.0/arcWidth**2.0))**0.5


mplt.plot(arcPoints)
mplt.ylim(0, 40)
mplt.show()