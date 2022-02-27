import importlib
import matplotlib.pyplot as plt

def twoPointNterp(p, vOne, vTwo):

    return ((1.0 - p) * vOne) + (p * vTwo)


########## ########## ########## ########## ##########

def thirdOrderLagrange(x, yn1, y0, y1, y2):
	
    z = x - 0.5; 

    even1 = yn1 + y2
    odd1 = yn1 - y2
    even2 = y0 + y1
    odd2 = y0 - y1

    c0 = ((9/16) * even2) - ((1/16) * even1)
    c1 = ((1/24) * odd1) - ((9/8) * odd2)
    c2 = ((1/4) * (even1 - even2))
    c3 = (0.5 * odd2 - ((1/6) * odd1))

    return ((c3 * z + c2) * z + c1) * z + c0

def cube(x, yn1, y0, y1, y2):

		p0 = yn1; p1 = y0; p2 = y1; p3 = y2
	
		a = -0.5*p0 + (1.5*p1) - (1.5*p2) + (1.5*p3)
		b = p0 - (2.5*p1) + (2.0*p2) - (0.5*p3)
		c = -0.5*p0 + (0.5*p2)
		d = p1
		
		return (a*x*x*x) + (b*x*x) + (c*x) + d
	
########## ########## ########## ########## ##########
########## ########## ########## ########## ##########

pointSet = [-1.5, -0.5, 0.3, -1.5, -0.5, 0.0, 3.5]
nPoints = len( pointSet ) - 1

#fine gradation (highly recommended to be a multiple of 4)
nSubPoint = 32; 

pInc = nPoints / (nPoints * nSubPoint)
pSetLen = nPoints * nSubPoint

iPointSet = [0.0] * pSetLen
temp = [0.0] * pSetLen

print( "len iPointSet", len(iPointSet) )

########## ########## ########## ########## ##########

p = 0.0
pointCount = 0
subpointCount = 0
counter = 1
cval = len( pointSet ) - 1

for i in range(0, nPoints - 1):
    
    for u in range(0, nSubPoint - 2):
     
       if p >= 1.0:
            p = p - 1.0
       
       
       if i == 1 or i == nPoints - 1:
            
            p0 = pointSet[i]
            p1 = pointSet[i + 1]

            iPointSet[counter] = twoPointNterp(p, p0, p1)
            temp[counter] = iPointSet[counter]
                        
       elif i > 1 and i <= (len(pointSet) - 2):
        
            pN = pointSet[i - 1]
            p0 = pointSet[i + 0]
            p1 = pointSet[i + 1]
            p2 = pointSet[i + 2] 
        
            iPointSet[counter] = cube(p, pN, p0, p1, p2)
            temp[counter] = iPointSet[counter]

       p += pInc
       counter += 1
       subpointCount += 1

    pointCount += 1


temp.sort()

plt.axis([ 0, nPoints, temp[0], temp[-1] ])
plt.plot(pointSet)

plt.show()
