import numpy as np

def circulantMatrices(cData):

  n = cData.shape[0]
  circulantMatrix = np.zeros([n, n])
  endIndices = list(range(n - 1, -1, -1))
  beginningIndices = []

  for i in range(n):
    endIndices.remove(i)
    beginningIndices = [i] + beginningIndices

    indices = beginningIndices + endIndices
    circulantMatrix[i] = cData.take(indices, mode='wrap')

  return circulantMatrix


C = np.array(range(20))
print(circulantMatrices(C))