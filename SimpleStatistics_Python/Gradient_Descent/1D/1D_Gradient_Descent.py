import numpy as np
import matplotlib.pyplot as plt

def gradientDescent(X, Y, L, maxIters):

  n = float(len(X))

  m = 0; c = 0
  for i in range(maxIters):
    predictedY = m*X + c
    D_m = (-2.0/n) * sum(X * (Y - predictedY))
    D_c = (-2.0/n) * sum(Y - predictedY)
    m = m - L*D_m
    c = c - L*D_c
  return m, c

eta = 0.1 #learning rate L
epochs = 300 #max iterations allowed

calculatedLineEQ = lambda x, m, b: m*x + b

nSteps = 100; xAxis = np.arange(0, 1, (1.0/nSteps)); testSlope = 0.5
testIntercept = 0.0
testData = [ calculatedLineEQ(i, testSlope, testIntercept) + (0.01 *
np.random.random()) for i in xAxis ]; #print(testData);

slope, intercept = gradientDescent(xAxis, testData, eta, epochs)
print(slope, intercept)

calculatedLineOutput = [ calculatedLineEQ(i, slope, intercept) for i in xAxis ]

ax = plt.subplot()
ax.plot(xAxis, calculatedLineOutput, label = 'line derived by gradient descent algorithm')
ax.scatter(xAxis, testData, alpha = 0.3, label = 'input data'); 
ax.legend()
plt.show()