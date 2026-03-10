import numpy as np

def pricingRequest(stockPrice, strikePrice, timeToMaturity, marketRate, marketVol, numOfSteps, isCall):
    deltaT = timeToMaturity/numOfSteps
    uVal  = np.e**(marketVol*(deltaT**(1/2)))
    dVal  = 1/uVal
    riskNuetralP = (np.e**(marketRate*deltaT)-dVal)/(uVal-dVal)
    discount = np.e**(-marketRate*deltaT)
    prices = []
    for i in range(numOfSteps+1):
        S = stockPrice * (uVal ** i) * (dVal ** (numOfSteps - i))
        prices.append(S)
    values = []
    vDown = 0
    vUp = 0
    for S in prices:
        if isCall:
            values.append(max(S - strikePrice, 0))
        else:
            values.append(max(strikePrice - S, 0))
    for i in range(numOfSteps -1,-1,-1):
        for j in range(i+1):
            values[j] = discount * (riskNuetralP * values[j+1] + (1-riskNuetralP) * values[j])
        if i == 1:
             vDown = values[0]
             vUp = values[1]
    sDown = stockPrice * dVal
    sUp = stockPrice * uVal
    delta = (vUp - vDown)/(sUp - sDown)
    price = values[0]
