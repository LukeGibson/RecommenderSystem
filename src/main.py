import numpy as np

def sim(u1, u2):
    return 0

# cur object is cursor for databases
def getPrediciton(userId, itemId, cur):
    # userRatings[0] = item, userRatings[1] = score
    ratingsDict = {}
    # Database call - given a userId get a list of (itemId, ratings) they've made
    criteria = (userId,)
    index = 0
    for row in cur.execute('SELECT itemID, rating FROM ratings WHERE userID = ?', criteria):
        ratingsDict.update({row[0]: row[1]})
    # return ratingsDict
    userItemRating = [(1, 4.5), (2, 1), (5, 2.5)]

    userItems = [i[0] for i in userItemRating]
    userRatings = [i[1] for i in userItemRating]

    # check user hasn't already reated item
    for item, rating in userItemRating:
        if itemId == item:
            return "Already rated: " + str(rating)

    # database call - given userItems get a list of userId's who also have a rating for at least 1 of the items
    userSubset = [2, 3, 4, 5, 6]

    # Initialise a list to store simScores
    simScores = []

    for user in userSubset:
        simScore = sim(userId, user)
        simScores.append((user, simScore))

    print(simScores)

    return "Not rated"

import sqlite3
connection = sqlite3.connect('../ratings.db')
cur = connection.cursor()
# for x,y in getPrediciton(1, 3, cur).items():
#     print(x, y)
# # print(pred)