import numpy as np
import math
import sqlite3
import os


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
    u1_ratings = []
    for i in range(len(shared_items)):
        criteria = (user_id, shared_items[i],)
        for row in cursor.execute('SELECT rating FROM ratings WHERE userID = ? AND itemID = ?', criteria):
            u1_ratings.append(row[0])

    user_id = u2
    u2_ratings = []
    for i in range(len(shared_items)):
        criteria = (user_id, shared_items[i],)
        for row in cursor.execute('SELECT rating FROM ratings WHERE userID = ? AND itemID = ?', criteria):
            u2_ratings.append(row[0])

    # given userId get a users average rating (rounded to 2dp)
    criteria = (u1,)
    for row in cursor.execute('SELECT AVG(rating) FROM ratings WHERE userID = ?', criteria):
        u1_avg = row[0]
    criteria = (u2,)
    for row in cursor.execute('SELECT AVG(rating) FROM ratings WHERE userID = ?', criteria):
        u2_avg = row[0]


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
    result = a / (b * c)

    return result


# calculate the predicted rating for user on item given a neighbourhood of similar users and their simScores
def pred(user_id, item_id, neighbours, cursor):
    # database call - given userId get a users average rating (rounded to 2dp)
    criteria = (user_id,)
    for row in cursor.execute('SELECT AVG(rating) FROM ratings WHERE userID = ?', criteria):
        u1_avg = row[0]

    a = 0
    b = 0

    for u2, u2_sim in neighbours:
        # database call - given userId get a users average rating (rounded to 2dp)
        criteria = (u2,)
        for row in cursor.execute('SELECT AVG(rating) FROM ratings WHERE userID = ?', criteria):
            u2_avg = row[0]

        # database call - given a userId and an itemId get the corresponding rating
        u2_item = None
        criteria = (u2, item_id)
        db_call = cursor.execute('SELECT rating FROM ratings WHERE userID = ? AND itemID = ?', criteria)
        for row in db_call:
            u2_item = row[0]
        
        # check u2 has rated that item, if so accumulate the scores
        if u2_item != None:
            a += u2_sim * (u2_item - u2_avg)
            b += u2_sim
    
    if b == 0:
        result = u1_avg
    else:
        result = u1_avg + (a / b)    

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
    user_ratings = [i[1] for i in user_item_rating]

    print("Items rated by user:", user_items)
    print("Ratings of user:", user_ratings)

    # check user hasn't already rated item
    for item, rating in user_item_rating:
        if item_id == item:
            print("User already rated this item!")
            return user_id, item_id, rating

    # database call - given userItems get a list of userId's who also have a rating for at least 1 of the items
    user_list = []
    for i in range(len(user_items)):
        criteria = (user_items[i],)
        for row in cursor.execute('SELECT userID FROM ratings WHERE itemID = ?', criteria):
            user_list.append(row[0])
    user_subset = list(dict.fromkeys(user_list))

    user_subset.remove(user_id)
    user_subset = user_subset[:50]

    print("Subset of users that share a rating:", user_subset)
    
    # Initialise a list to store simScores
    sim_scores = []

    for compare_user_id in user_subset:
        sim_score = sim(user_id, compare_user_id, cursor)
        sim_scores.append((compare_user_id, sim_score))
    
    print("Similarity scores between user and user subset:", sim_scores)

    # select the neighbourhood topN most similar users from the userSubset
    neighbours = []
    topN = int(len(sim_scores) / 2)

    print("topN:", topN)

    # orders the sim_scores in accending order - then takes the sim_score indexes of the last N elements: N most similar users.
    user_indexs = np.argsort([score[1] for score in sim_scores])[-topN:]

    for index in user_indexs:
        neighbours.append(sim_scores[index])
    
    print("Users most similar neighbours:", neighbours)

    # calculate the prediction
    predRating = pred(user_id, item_id, neighbours, cursor)

    return user_id, item_id, predRating