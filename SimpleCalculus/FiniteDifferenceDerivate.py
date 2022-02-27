def function(x):
    return x**2

def derivative(a, b):
    return function(b) - function(a) / (b - a)
    
testValue = derivative(0.0, 1.0)

print("testValue =", testValue)