import numpy as np
import math

def sim(u1, u2):
    # database call - given 2 userId's return the list of itemId's they've both rated
    sharedItems = [1, 4, 5]

    # database call - given a userId and the sharedItems return the list of ratings
    u1Ratings = [8, 2, 7]
    u2Ratings = [2, 7, 5]

    # database call - given userId get a users average rating (rounded to 2dp)
    u1Avg = 5.7
    u2Avg = 4.75

    # accumulator for 3 parts of sim equation
    a = 0
    b = 0
    c = 0

    for i in range(len(sharedItems)):
        ratingU1 = u1Ratings[i] - u1Avg
        ratingU2 = u2Ratings[i] - u2Avg

        ratingU1Sq = ratingU1 * ratingU1
        ratingU2Sq = ratingU2 * ratingU2

        a += ratingU1 * ratingU2
        b += ratingU1Sq
        c += ratingU2Sq

    b = math.sqrt(b)
    c = math.sqrt(c)

    result = a / (b * c)

    return result


def getPrediciton(userId, itemId):
    # database call - given a userId get a list of (itemId, ratings) they've made
    userItemRating = [(1, 4.5), (2, 1), (5, 2.5)]

    userItems = [i[0] for i in userItemRating]
    userRatings = [i[1] for i in userItemRating]

    # check user hasn't already reated item
    for item, rating in userItemRating:
        if itemId == item:
            return  ("Already rated: " + str(rating))
    
    # database call - given userItems get a list of userId's who also have a rating for at least 1 of the items
    userSubset = [2, 3, 4, 5, 6]

    #initalise a list to store simScores
    simScores = []

    for user in userSubset:
        simScore = sim(userId, user)
        simScores.append((user, simScore))

    print(simScores)

    return "Not rated"


# pred = getPrediciton(1, 3)
# print(pred)

print(sim(0,0))