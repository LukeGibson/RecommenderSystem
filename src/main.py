import numpy as np
import math
import sqlite3
connection = sqlite3.connect('../ratings.db')
cur = connection.cursor()


# uses the Pearson coefficient to calculate the similarity between 2 users
def sim(u1, u2, cursor):
    # given 2 userId's return the list of itemId's they've both rated
    id_1 = (u1,)
    id_2 = (u2,)
    ratings1 = []
    ratings2 = []
    for row in cursor.execute('SELECT itemID FROM ratings WHERE userID = ?', id_1):
        ratings1.append(row[0])
    for row in cursor.execute('SELECT itemID FROM ratings WHERE userID = ?', id_2):
        ratings2.append(row[0])
    shared_items = [v for v in ratings1 if v in ratings2]

    # given a userId and the sharedItems return the list of ratings
    user_id = u1
    ratings = []
    for i in range(len(shared_items)):
        criteria = (user_id, shared_items[i],)
        for row in cursor.execute('SELECT rating FROM ratings WHERE userID = ? AND itemID = ?', criteria):
            ratings.append(row[0])
    u1_ratings = ratings
    u2_ratings = [2, 7, 5]

    # given userId get a users average rating (rounded to 2dp)
    user_id = 1
    criteria = (user_id,)
    rating = 0
    for row in cursor.execute('SELECT AVG(rating) FROM ratings WHERE userID = ?', criteria):
        rating = round(row[0], 2)
    # return ratingsDict
    u1_avg = rating
    u2_avg = 4.75

    # accumulator for 3 parts of sim equation
    a, b, c = 0, 0, 0

    for i in range(len(shared_items)):
        rating_u1 = u1_ratings[i] - u1_avg
        rating_u2 = u2_ratings[i] - u2_avg

        rating_u1_sq = rating_u1 * rating_u1
        rating_u2_sq = rating_u2 * rating_u2

        a += rating_u1 * rating_u2
        b += rating_u1_sq
        c += rating_u2_sq

    b = math.sqrt(b)
    c = math.sqrt(c)

    # round the equation output to 3 decimal places
    result = round(a / (b * c), 3)

    return result


# cur object is cursor for databases
def get_prediction(user_id, item_id, cursor):
    # userRatings[0] = item, userRatings[1] = score
    ratings_dict = {}
    # given a userId get a list of (itemId, ratings) they've made
    criteria = (user_id,)
    for row in cursor.execute('SELECT itemID, rating FROM ratings WHERE userID = ?', criteria):
        ratings_dict.update({row[0]: row[1]})

    user_item_rating = ratings_dict.items()
    user_items = [i[0] for i in user_item_rating]
    print(user_items)
    user_ratings = [i[1] for i in user_item_rating]
    print(user_ratings)

    # check user hasn't already rated item
    for item, rating in user_item_rating:
        if item_id == item:
            return "Already rated: " + str(rating)

    # database call - given userItems get a list of userId's who also have a rating for at least 1 of the items
    item_list = [12793, 113, 1876]
    user_list = []
    for i in range(len(item_list)):
        criteria = (item_list[i],)
        for row in cursor.execute('SELECT userID FROM ratings WHERE itemID = ?', criteria):
            user_list.append(row[0])
    user_subset = list(dict.fromkeys(user_list))

    # Initialise a list to store simScores
    sim_scores = []

    for user in user_subset:
        sim_score = sim(user_id, user, cursor)
        sim_scores.append((user, sim_score))

    # print(sim_scores)

    return "Not rated"
