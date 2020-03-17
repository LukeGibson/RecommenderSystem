import numpy as np
import math
import time


# uses the Pearson coefficient to calculate the similarity between 2 users
# user_ratings_dict = {item_id, rating}
def sim(user_ratings_dict, user_subset, cursor):
    # given userId get a users average rating (rounded to 2dp)
    u1_avg = sum(user_ratings_dict.values()) / len(user_ratings_dict)

    sim_scores = []

    count = 0

    for u2 in user_subset:
        u2_ratings_dict = {}

        if count < 5:
            db_start = time.time()
        for row in cursor.execute(f'SELECT itemID, rating FROM {table_name} WHERE userID = ?', (u2,)):
            u2_ratings_dict.update({row[0]: row[1]})
        if count < 5:
            db_end = time.time()
        shared_items = [v for v in user_ratings_dict if v in u2_ratings_dict]
        # given a userId and the sharedItems return the list of ratings

        u2_avg = sum(u2_ratings_dict.values()) / len(u2_ratings_dict)
        # accumulator for 3 parts of sim equation
        a, b, c = 0, 0, 0


        for item in shared_items:
            rating_u1 = user_ratings_dict[item] - u1_avg
            rating_u2 = u2_ratings_dict[item] - u2_avg

            rating_u1_sq = rating_u1 * rating_u1
            rating_u2_sq = rating_u2 * rating_u2

            a += rating_u1 * rating_u2
            b += rating_u1_sq
            c += rating_u2_sq

        b = math.sqrt(b)
        c = math.sqrt(c)

        if count < 5:
            print("DB call time:", db_end - db_start)

        # round the equation output to 3 decimal places
        sim_scores.append((u2, a / (b * c)))

    return sim_scores


# calculate the predicted rating for user on item given a neighbourhood of similar users and their simScores
def pred(user_ratings_dict, item_id, neighbours, cursor):

    u1_avg = sum(user_ratings_dict.values()) / len(user_ratings_dict)

    a = 0
    b = 0

    for u2, u2_sim in neighbours:
        # database call - given userId get a users average rating (rounded to 2dp)
        u2_ratings_dict = {}
        for row in cursor.execute(f'SELECT itemID, rating FROM {table_name} WHERE userID = ?', (u2,)):
            u2_ratings_dict.update({row[0]: row[1]})

        u2_avg = sum(u2_ratings_dict.values()) / len(u2_ratings_dict)
        
        # check u2 has rated that item, if so accumulate the scores
        if item_id in u2_ratings_dict:
            a += u2_sim * (u2_ratings_dict[item_id] - u2_avg)
            b += u2_sim
    
    if b == 0:
        result = u1_avg
    else:
        result = u1_avg + (a / b)    

    return result


# cur object is cursor for databases
def get_prediction(user_id, item_id, table_nm, cursor):
    global table_name
    table_name = table_nm
    # userRatings[0] = item, userRatings[1] = score
    ratings_dict = {}
    # given a userId get a list of (itemId, ratings) they've made
    criteria = (user_id,)
    for row in cursor.execute(f'SELECT itemID, rating FROM {table_name} WHERE userID = ?', criteria):
        ratings_dict.update({row[0]: row[1]})


    # check user hasn't already rated item
    for item, rating in ratings_dict.items():
        if item_id == item:
            print("User already rated this item!")
            return user_id, item_id, rating

    # database call - given userItems get a list of userId's who also have a rating for at least 1 of the items
    # userID and all the items they've rated, then look to see how of these are one of the items our user has rated
    thresh = 30 if len(ratings_dict.items()) > 30 else len(ratings_dict.items())
    # print("Thresh:", thresh)
    user_item_count = {}
    for row in cursor.execute(f"SELECT userID FROM {table_name} WHERE itemID IN ({','.join(map(str, ratings_dict.keys()))}) "):
        user_item_count[row[0]] = user_item_count.get(row[0], 0) + 1

    user_subset = []
    for x, y in user_item_count.items():
        if y >= thresh:
            user_subset.append(x)
    user_subset.remove(user_id)
    before = len(user_item_count) - 1
    after = len(user_subset)
    print("Users before:", before, ", Users after:", after, ", Difference:", before - after)

    #print("User Subset", user_subset)

    # Initialise a list to store simScores
    time_a = time.time()
    sim_scores = sim(ratings_dict, user_subset, cursor)
    time_b = time.time()
    print("Average sim time:", (time_b - time_a)/len(sim_scores))
    # for compare_user_id in user_subset:
    #     sim_score = sim(user_id, compare_user_id, cursor)
    #     sim_scores.append((compare_user_id, sim_score))
    
    print("Similarity scores between user and user subset:", sim_scores)

    # select the neighbourhood topN most similar users from the userSubset
    neighbours = []
    topN = 12_000 if len(sim_scores) > 12_000 else len(sim_scores)
    # if < 2500 keep all, form 2000, 12000 scale, never more than 12,000

    print("topN:", topN)

    # orders the sim_scores in accending order - then takes the sim_score indexes of the last N elements: N most similar users.
    user_indexs = np.argsort([score[1] for score in sim_scores])[-topN:]

    for index in user_indexs:
        neighbours.append(sim_scores[index])
    
    print("Users most similar neighbours:", neighbours)

    time_a = time.time()
    result = pred(ratings_dict, item_id, neighbours, cursor)
    time_b = time.time()
    print("Pred time per neighbour:", (time_b - time_a)/len(neighbours))
    return result