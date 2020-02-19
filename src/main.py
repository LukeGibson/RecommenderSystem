import numpy as np

def sim(u1, u2):
    return 0


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


pred = getPrediciton(1, 3)
print(pred)