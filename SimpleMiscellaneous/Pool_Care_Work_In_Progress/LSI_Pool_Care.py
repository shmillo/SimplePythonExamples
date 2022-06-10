def afLUT(TA):

    AF = 0.0

    if(TA >= 0 and TA <= 25):
        AF = 0.7
    elif(TA > 25 and TA <= 50):
        AF = 1.4
    elif(TA > 50 and TA <= 75):
        AF = 1.9
    elif(TA > 75 and TA <= 100):
        AF = 2.0
    elif(TA > 100 and TA <= 150):
        AF = 2.2
    elif(TA > 150 and TA <= 200):
        AF = 2.3
    elif(TA > 200 and TA <= 300):
        AF = 2.5
    elif(TA > 300 and TA <= 400):
        AF = 2.6
    elif(TA > 400 and TA <= 800):
        AF = 2.9
    elif(TA > 800 and TA <= 1000):
        AF = 3.0
    return AF

def cfLUT(CH):

    CF = 0.0

    if(CH >= 0 and CH <= 5):
        CF = 0.3
    elif(CH > 5 and CH <= 25):
        CF = 1.0
    elif(CH > 25 and CH <= 50):
        CF = 1.3
    elif(CH > 50 and CH <= 75):
        CF = 1.5
    elif(CH > 75 and CH <= 100):
        CF = 1.6
    elif(CH > 100 and CH <= 150):
        CF = 1.8
    elif(CH > 150 and CH <= 200):
        CF = 1.9
    elif(CH > 200 and CH <= 300):
        CF = 2.1
    elif(CH > 300 and CH <= 400):
        CF = 2.2
    elif(CH > 400 and CH <= 800):
        CF = 2.5
    elif(CH > 800 and CH <= 1000):
        CF = 2.6

    return CF

def tfLUT(Temp):

    TF = 0.0

    if(Temp >= 0 and Temp <= 32):
        TF = 0.0
    elif(Temp > 32 and Temp <= 37):
        TF = 0.1
    elif(Temp > 37 and Temp <= 46):
        TF = 0.2
    elif(Temp > 46 and Temp <= 53):
        TF = 0.3
    elif(Temp > 53 and Temp <= 60):
        TF = 0.4
    elif(Temp > 60 and Temp <= 66):
        TF = 0.5
    elif(Temp > 66 and Temp <= 76):
        TF = 0.6
    elif(Temp > 76 and Temp <= 84):
        TF = 0.7
    elif(Temp > 84 and Temp <= 94):
        TF = 0.8
    elif(Temp > 94 and Temp <= 105):
        TF = 0.9
    else:
        TF = 1.0
        
    return TF

def tdsfLUT(TDS):
    tdsf = 0.0
    if(TDS > 0 and TDS <= 1000):
        tdsf = 12.1
    else:
        tdsf = 12.2
    return tdsf

def cyaLUT(pH, CYA):

    factor = 0.0
    if(pH <= 7.0):
        factor = 0.23
    elif(pH > 7.0 and pH <= 7.2):
        factor = 0.27
    elif(pH > 7.2 and pH <= 7.4): 
        factor = 0.31
    elif(pH > 7.4 and pH <= 7.6):
        factor = 0.33
    elif(pH > 7.6 and pH <= 7.8):
        factor = 0.35
    elif(pH > 7.8 and pH <= 8.0):
        factor = 0.36
    
    return CYA * factor

def langelierLUT(pH, TA, CH, temp, TDS, CYA, isTAA):

    #clamp pH values just in case
    if(pH < 6.4):
        pH = 6.4
    elif(pH > 8.9):
        pH = 8.9
    
    AF = afLUT(TA)
    cyaCF = cyaLUT(pH, CYA)
    CF = cfLUT(CH)
    TF = tfLUT(temp)
    TDSf = tdsfLUT(TDS)

    lsiVector = [pH, AF, CF, TF, TDSf]

    lsiTemp = 0.0
    if(isTAA or AF < 50.0):
        #use adjusted Alkalinity factor if desired (or if low)
        lsiTemp = pH + (AF - cyaCF) + CF + TF - TDSf
    else:
        lsiTemp = pH + AF + CF + TF - TDSf

    return float(lsiTemp), lsiVector

#####################################################################################
#####################################################################################
#####################################################################################

def liquidAmt(DeltaC, poolSize):
    #FAC per dose
    freeChlorineDose = 11.0
    #number of doses needed to achieve DeltaC at the per 10000g amt, * the size scalar
    neededDoses = (DeltaC / freeChlorineDose) * (poolSize / 10000.0)
    #avoid recommending less than one gallon
    if(neededDoses > 0.0 and neededDoses < 1.0):
        neededDoses = 1.0
    return round(neededDoses)

def burnoutAmt(DeltaC, poolSize):
    #FAC per dose
    freeChlorineDose = 7.0; chDose = 5.5
    #number of doses needed to achieve DeltaC at the per 10000g amt, * the size scalar
    neededDoses = (DeltaC / freeChlorineDose) * (poolSize / 12000.0)
    #dont recommend less than one package
    if(neededDoses > 0.0 and neededDoses < 1.0):
        neededDoses = 1.0
    return round(neededDoses)

def oxyAmt(DeltaC, poolSize):
    #Chloramine reduction per dose
    chloramineGasOffDose = 0.4
    #number of doses needed to achieve DeltaC at the per 10000g amt, * the size scalar
    neededDoses = (DeltaC / chloramineGasOffDose) * (poolSize / 10000.0)
    #dont recommend less than one package
    if(neededDoses > 0.0 and neededDoses < 1.0):
        neededDoses = 1.0
    return round(neededDoses)

def chlorineRecommendation(poolTotalChlorine, poolFreeChlorine, poolSize):

    DeltaC = 0.0; doseLiquid = 0.0; doseBurnout = 0.0; doseOxy = 0.0

    #if chloramines are present in the pool
    if(poolFreeChlorine != poolTotalChlorine):
        #if the residual is within a safe range
        if(poolFreeChlorine > 0.0 and poolFreeChlorine <= 4.0):
            #Breakpoint Chlorination
            BPC = (10.0 * (poolTotalChlorine - poolFreeChlorine))
            #Change in FAC chlorine needed to gas off chloramines present in water
            DeltaC = BPC - poolFreeChlorine
            #if a large/direct amount of FAC is needed
            if(DeltaC > 6.0): 
                doseLiquid = liquidAmt(DeltaC, poolSize)
                doseBurnout = burnoutAmt(DeltaC, poolSize)

        #if the residual is above a safe range, use oxy plus
        if(poolFreeChlorine > 4.0):
            BPC = (10.0 * (poolTotalChlorine - poolFreeChlorine))
            DeltaC = BPC - poolFreeChlorine
            doseOxy = oxyAmt(DeltaC)

    #if FAC = TC, simply achieve the residual needed
    elif(poolFreeChlorine < 1.0):
        DeltaC = 4.0 - poolFreeChlorine
        doseLiquid = liquidAmt(DeltaC, poolSize)
        doseBurnout = burnoutAmt(DeltaC, poolSize)

    #if FAC = TC, but both are high, wait a week for residual to drop
    elif(poolFreeChlorine > 4.0):
        DeltaC = 0.0

    return doseLiquid, doseBurnout, doseOxy

#####################################################################################
#####################################################################################
#####################################################################################

def doseAlkalinity(poolSize, desiredTA, currentTA):
    return ((desiredTA - currentTA) / 10.0) * 1.5 * (poolSize/10000.0)

def bakingSodaPHIncrease(doseBakingSoda, poolSize):
    amountToIncreaseOneDecimal = ((0.3 * (10000.0 / 500.0)) * (poolSize / 10000.0))
    numberOfDecimalsIncreased = doseBakingSoda / amountToIncreaseOneDecimal
    if(numberOfDecimalsIncreased > 1.0):
        temporary = 0.0
        for i in range(numberOfDecimalsIncreased):
            temporary += 0.1
    return temporary

#####################################################################################
#####################################################################################
#####################################################################################

def productRecommendation(poolSatIndex, factorVector, poolSize, poolTotalChlorine, poolFreeChlorine, poolPH, poolTA, poolCH, poolTemp, poolTDS, poolCYA):
    
    doseBakingSoda = 0.0; doseCalciumCarbonate = 0.0; doseLS = 0.0; doseBO = 0.0; doseOP = 0.0

    #saturation index indicates corrosive water
    if(poolSatIndex < -0.3):

        #pH Demand, half-life of hypochlorous acid cut in half, need to address before moving forward
        if(factorVector[0] < 6.6):
            if(factorVector[1] < 2.2):
                doseBakingSoda = doseAlkalinity(poolSize, 150, poolTA)
                factorVector[0] += bakingSodaPHIncrease(doseBakingSoda, poolSize)

        #pH is Low, could be harmful to younger swimmers or equipment
        elif(factorVector[0] > 6.6 and factorVector[0] < 7.3):

            if(factorVector[1] < 2.2):
                doseBakingSoda = doseAlkalinity(poolSize, 150, poolTA)
                factorVector[0] += bakingSodaPHIncrease(doseBakingSoda, poolSize)

            [doseLS, doseBO, doseOP] = chlorineRecommendation(poolTotalChlorine, poolFreeChlorine, poolSize)

        #saturation index indicates potential for scale-forming water        
        elif(poolSatIndex > 0.3):
            if(factorVector[1] < 2.2):
                doseBakingSoda = doseAlkalinity(poolSize, 150, poolTA)
                factorVector[0] += bakingSodaPHIncrease(doseBakingSoda, poolSize)
            [doseLS, doseBO, doseOP] = chlorineRecommendation(poolTotalChlorine, poolFreeChlorine, poolSize)

        #saturation index within an acceptable range for residential pools
        elif(poolSatIndex >= -0.3 and poolSatIndex <= 0.3):
            [doseLS, doseBO, doseOP] = chlorineRecommendation(poolTotalChlorine, poolFreeChlorine, poolSize)

    return doseBakingSoda, doseCalciumCarbonate, doseLS, doseBO, doseOP

#####################################################################################
#####################################################################################
#####################################################################################

poolSize = 20000.0; poolPH = 8.6; poolTA = 60; poolCH = 125; 
poolTemp = 71; poolTDS = 2500; poolCYA = 41; 

poolTotalChlorine = 11.0; poolFreeChlorine = 0.1

#####################################################################################

poolSatIndex, factorVector = langelierLUT(poolPH, poolTA, poolCH, poolTemp, poolTDS, poolCYA, 0)

productRecommendation(poolSatIndex, factorVector, poolSize, poolTotalChlorine, poolFreeChlorine, poolPH, poolTA, poolCH, poolTemp, poolTDS, poolCYA)

print( poolSatIndex )
  
