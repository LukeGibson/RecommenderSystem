import numpy as np
import math
import sqlite3


# uses the Pearson coefficient to calculate the similarity between 2 users
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
    a, b, c = 0, 0, 0

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

    # round the equation output to 2 decimal places
    result = round(a / (b * c), 2)

    return result


# calculate the predicted rating for user on item given a neighbourhood of similar users and their simScores
def pred(userId, itemID, neighbours):
    # database call - given userId get a users average rating (rounded to 2dp)
    u1Avg = 5.7

    a = 0
    b = 0

    for u2, u2Sim in neighbours:
        # database call - given userId get a users average rating (rounded to 2dp)
        u2Avg = 3.4
        # database call - given a userId and an itemId get the corresponding rating
        u2Item = 4.5
        
        # check u2 has rated that item, if so accumulate the scores
        if u2Item != None:
            a += u2Sim * (u2Item - u2Avg)
            b += u2Sim
    
    # round the equation output to 2 decimal places
    result = round(u1Avg + (a / b), 2)


# cur object is cursor for databases
def getPrediciton(userId, itemId, cur):
    # userRatings[0] = item, userRatings[1] = scores
    ratingsDict = {}
 
    # Database call - given a userId get a list of (itemId, ratings) they've made
    criteria = (userId,)
    index = 0
    for row in cur.execute('SELECT itemID, rating FROM ratings WHERE userID = ?', criteria):
        ratingsDict.update({row[0]: row[1]})
    # return ratingsDict
    userItemRating = ratingsDict.items()
    # print(userItemRating)

    userItems = [i[0] for i in userItemRating]
    print(userItems)
    userRatings = [i[1] for i in userItemRating]
    print(userRatings)

    # check user hasn't already reated item
    for item, rating in userItemRating:
        if itemId == item:
            return "Already rated: " + str(rating)

    # database call - given userItems get a list of userId's who also have a rating for at least 1 of the items
    userSubset = [2, 3, 4, 5, 6]

    # Initialise a list to store simScores
    simScores = []

    # calculate users similarities
    for user in userSubset:
        simScore = sim(userId, user)
        simScores.append((user, simScore))

    # select the neighbourhood topN most similar users from the userSubset
    neighbours = []
    topN = 3

    userIndexs = np.argsort(simScores)[-topN:]

    for index in userIndexs:
        neighbours.append((userSubset[index], simScores[index]))

    # calculate the prediction
    predRating = pred(userId, itemId, neighbours)

    return "Predicted rating:" + str(predRating)


# connection = sqlite3.connect('../ratings.db')
# cur = connection.cursor()
# print(getPrediciton(1,5,cur))