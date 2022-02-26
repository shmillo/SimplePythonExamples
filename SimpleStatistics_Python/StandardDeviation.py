testData = [10, 6, -7, -20, 15, 105, 2000]
length = len(testData)

mean = 0.0
for i in range(length):
    mean += testData[i]
mean /= length
print("mean")
print(mean)

variance = 0.0
for i in range(length):
    variance += (testData[i] - mean)**2
variance /= length
print("variance")
print(variance)

standardDeviation = variance**0.5
print("standardDeviation")
print(standardDeviation)