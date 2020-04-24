import numpy as np
import math
import time

u1 = [8,-1,-1,2,7]
u2 = [2,-1,5,7,5]
u3 = [5,4,7,4,7]

u1t = [1584547289,-1,-1,1584547289,1584547289] # 2020
u2t = [827164832,-1,827164832,827164832,827164832] # 1996
u3t = [1268928032,1268928032,1268928032,1268928032,1268928032] # 2010

def sim(u1, u2):
    # get average ratings and items both users have rated
    u1Av = 0
    u2Av = 0

    u1Count = 0
    u2Count = 0

    sharedItems = []

    for i in range(len(u1)):
        u1R = u1[i]
        u2R = u2[i]

        if u1R != -1:
            u1Av += u1R
            u1Count += 1
        if u2R != -1:
            u2Av += u2R
            u2Count += 1
        
        if u2R != -1 and u1R != -1:
            sharedItems.append(i)
    
    u1Av = u1Av / u1Count
    u2Av = u2Av / u2Count

    # print("u1Av:", u1Av)
    # print("u2Av:", u2Av)
    # print("Shared Items:", sharedItems)

    # get top of sim equation 'a'
    a = 0

    for item in sharedItems:
        u1R = u1[item]
        u2R = u2[item]

        acc = (u1R - u1Av) * (u2R - u2Av)

        a += acc
    
    # print("A:", a)

    # get bottom of sim equation 'b' and 'c'
    b = 0
    c = 0

    for item in sharedItems:
        u1R = u1[item]
        u2R = u2[item]

        accB = (u1R - u1Av)**2

        b += accB
        
        accC = (u2R - u2Av)**2

        c += accC

    b = math.sqrt(b)
    c = math.sqrt(c)

    # print("B:", b)
    # print("C:", c)

    result = a / (b * c)
    # print("SimScore:", result)

    return (result, u2Av)


def pred(u1, n, nt, item):
    simScores = []
    u2Avs = []

    for u2 in n:
        simScore, u2Av = sim(u1, u2)
        simScores.append(simScore)
        u2Avs.append(u2Av)

    # get top of pred equation 'a' and bottom 'b'
    currTime = time.time()
    a = 0
    b = 0

    for i in range(len(n)):
        u2 = n[i]
        u2t = nt[i]
        simScore = simScores[i]
        u2Av = u2Avs[i]

        # calculate the rating age        
        ratingAge = currTime - u2t[item]
        ageWeight = getAgeWeight(ratingAge)
        print("Age Weight:", ageWeight)

        # factor in a weighting on the rating age
        accA = ageWeight * simScore * (u2[item] - u2Av)
        a += accA

        accB = ageWeight * simScore
        b += accB

    # calculate u1Av
    u1Av = 0
    u1Count = 0

    for i in range(len(u1)):
        u1R = u1[i]

        if u1R != -1:
            u1Av += u1R
            u1Count += 1
    
    u1Av = u1Av / u1Count
    
    print(u1Av, a/b)

    result = u1Av + (a / b)
    print(result)


def getAgeWeight(age):
    # convert age from seconds to years
    age = age / 31536000
    print("Age:", age)

    # set thresholds and their weight values
    highThres = 2
    highWeight = 1

    lowThres = 20
    lowWeight = 0.25

    if age < highThres:
        weight = highWeight
    elif age > lowThres:
        weight = lowWeight
    else:
        grad = (highWeight - lowWeight) / (highThres - lowThres)
        weight = (grad*(age - highThres)) + 1
    
    return weight


pred(u1, [u2, u3], [u2t, u3t], 2)