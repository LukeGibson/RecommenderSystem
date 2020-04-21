import numpy as np
import math
import time


def make_table_name(x):
    return "users_to_" + str(int(math.ceil(int(x) / 5_000)) * 5000) + "_ratings"


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
        table_name = make_table_name(u2)
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
            print("DB call time:", db_end - db_start, "Dict size:", len(u2_ratings_dict))

        sim_scores.append((u2, a / (b * c)))

    return sim_scores

# given an age of a rating in seconds calculates its relavence as a wighting from 0 to 1
def get_age_weight(age):
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


# calculate the predicted rating for user on item given a neighbourhood of similar users and their simScores
def pred(user_ratings_dict, item_id, neighbours, cursor):
    curr_time = time.time()
    u1_avg = sum(user_ratings_dict.values()) / len(user_ratings_dict)

    a = 0
    b = 0

    for u2, u2_sim in neighbours:
        # database call - given userId get a users average rating (rounded to 2dp)
        u2_ratings_dict = {}
        table_name = make_table_name(u2)
        for row in cursor.execute(f'SELECT itemID, rating FROM {table_name} WHERE userID = ?', (u2,)):
            u2_ratings_dict.update({row[0]: row[1]})

        u2_avg = sum(u2_ratings_dict.values()) / len(u2_ratings_dict)

        # GET THE TIMESTAMP FOR U2's RATING OF ITEM_ID 
        time_stamp = 1584547289 # have set to 18/03/20
        rating_age = curr_time - time_stamp
        age_weight = get_age_weight(rating_age)

        # check u2 has rated that item, if so accumulate the scores
        if item_id in u2_ratings_dict:

            a += age_weight * u2_sim * (u2_ratings_dict[item_id] - u2_avg)
            b += age_weight * u2_sim
    
    if b == 0:
        result = u1_avg
    else:
        result = u1_avg + (a / b)    

    return result


# cur object is cursor for databases
def get_prediction(user_id, item_id, large_table_name, cursor):
    # userRatings[0] = item, userRatings[1] = score
    ratings_dict = {}
    # given a userId get a list of (itemId, ratings) they've made
    criteria = (user_id,)
    table_name = make_table_name(user_id)
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
    table_name = make_table_name(user_id)
    for row in cursor.execute(f"SELECT userID FROM {large_table_name} WHERE itemID IN ({','.join(map(str, ratings_dict.keys()))}) "):
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