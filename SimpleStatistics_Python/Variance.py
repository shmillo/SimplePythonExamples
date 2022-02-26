testData = [5, 6, 8, 9, 10, 11, 14]

length = len(testData)

mean = 0.0
for i in range(length):
    mean = mean + testData[i]
mean /= length

print("mean:")
print(mean)

variance = 0.0
for i in range(length):
    variance = variance + ( testData[i] - mean )**2
variance /= (length - 1)

print("variance:")
print(variance)