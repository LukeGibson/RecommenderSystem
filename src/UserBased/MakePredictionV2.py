import numpy as np
from math import sqrt, pow
from time import time
import pandas as pd


# uses the pearson coefficient to calculate the similarity between 2 users
def calc_sim_scores(df, u1, user_subset):
    
    # average rating for u1
    u1_avg = df.loc[u1]['rating'].mean() 
    # all items user 1 rated
    u1_items = [y for x, y in df.index if x == u1] 
    # list of (user, simScore) we eventually return
    sim_scores = [] 

    # loop through users who have rated some of the same items to u1
    for u2 in user_subset:

        # get ites u2 and u1 both rated
        u2_items = [y for x, y in df.index if x == u2] 
        shared_items = [s for s in u1_items if s in u2_items] 

        # average rating for u2
        u2_avg = df.loc[u2]['rating'].mean()

        # accumulator for 3 parts of sim equation
        a, b, c = 0, 0, 0

        # loop through each of the items u1 and u2 rated
        for item in shared_items:
            
            # calculate the difference from their average rating
            rating_u1 = df.loc[(u1, item)]['rating'] - u1_avg
            rating_u2 = df.loc[(u2, item)]['rating'] - u2_avg

            # accumulate the seperate sums of the sim equation
            a += (rating_u1 * rating_u2)
            b += pow(rating_u1, 2)
            c += pow(rating_u2, 2)

        # finish the operations outside of the sim equation sums
        b = sqrt(b)
        c = sqrt(c)

        # check for divide by 0 error
        score = 0 if b == 0 or c == 0 else (a/(b*c))

        # add the calulated simScore for u2 to returning list
        sim_scores.append((u2, score))

    return sim_scores



# calculate the predicted rating for user on item given a neighbourhood of similar users and their simScores
def pred(df, u1, item_id, neighbours):

    # u1 average rating
    u1_avg = df.loc[u1]['rating'].mean() 
    
    # accumulators for pred equation
    a, b = 0, 0

    # loop through neighbours
    for u2, u2_sim in neighbours:

        # neighbours average rating 
        u2_avg = df.loc[u2]['rating'].mean()

        # check neighbour has rated item being predicted
        if (u2, item_id) in df.index:
            # accumulate seperate sums of the pred equation
            a += (u2_sim * (df.loc[(u2, item_id)]['rating'] - u2_avg))
            b += u2_sim

    # checks for a divide by 0 error
    predict = u1_avg if b == 0 else u1_avg + (a/b)

    # clamps predict within 0 and 5
    # predict = max(0, min(5, predict))

    # Return None, done to see how good the normal predictions are
    if predict > 5 or predict < 0:
        return None
    else:
        return predict


# returns a list of predicitons of user_id on the items in the item_list such that order is maintained
def get_prediction(user_id, item_list, user_table_nm, item_list_dict, cursor):
    # s = time()

    # given a userId create a dataframe of all their ratings
    df = pd.DataFrame(columns=['userID', 'itemID', 'rating', 'time']).set_index(['userID', 'itemID'])
    user_dict = {"userID": [], "itemID": [], "rating": [], "time": []}

    for row in cursor.execute(f'SELECT itemID, rating, time FROM {user_table_nm} WHERE userID = ?', (user_id,)):
        user_dict["userID"].append(user_id)
        user_dict["itemID"].append(row[0])
        user_dict["rating"].append(row[1])
        user_dict["time"].append(row[2])
    df = df.append(pd.DataFrame.from_dict(user_dict).set_index(['userID', 'itemID']))

    # print("First DB call", (time() - s))
    # s = time()


    # list of all items u1 rated
    items_rated = [y for x, y in df.index]
    user_item_count = {}
    # dictionary: counts each user to how many times they've rated an item that u1 rated
    for item in items_rated:
        for user in item_list_dict[item]:
            user_item_count[user] = user_item_count.get(user, 0) + 1

    # number of top users to select
    user_subset = []
    max_user_size = 40 

    # order dictionary and select the top users
    for k, v in sorted(user_item_count.items(), key=lambda item: item[1], reverse=True):
        if len(user_subset) < max_user_size and not k == user_id:
            user_subset.append(k)


    # print("Second DB call", (time() - s))
    # s = time()


    # for the filtered top users get all of their details
    user_dict = {"userID": [], "itemID": [], "rating": [], "time": []}
    for row in cursor.execute(f"SELECT userID, itemID, rating, time FROM {user_table_nm} WHERE userID IN ({','.join(map(str, user_subset))})"):
        user_dict["userID"].append(row[0])
        user_dict["itemID"].append(row[1])
        user_dict["rating"].append(row[2])
        user_dict["time"].append(row[3])
    df = df.append(pd.DataFrame.from_dict(user_dict).set_index(['userID', 'itemID']))


    # print("Third DB call", (time() - s))
    # s = time()


    # check the user subset still contains users after filtering 
    if len(user_subset) == 0: 
        # (NEED TO FIGURE OUT WHAT TO DO IN THIS CASE)
        return None

    # calculate users similarity to each user in subset
    sim_scores = calc_sim_scores(df, user_id, user_subset)
    # filters returned simScores to only show positive 
    pos_sim_scores = [x for x in sim_scores if x[1] > 0] 


    # print("Sim time: ", (time() - s))
    # s = time()


    # create neighbours list as top N most similar users
    neighbours = [] 
    topN = 12_000 if len(pos_sim_scores) > 12_000 else len(pos_sim_scores)
    user_indexes = np.argsort([score[1] for score in pos_sim_scores])[-topN:]
    for index in user_indexes:
        neighbours.append(pos_sim_scores[index])


    # loop through items to predict for the input user
    results = [] 
    for item_id in item_list:
        # check if user has already rated item
        if (user_id, item_id) in df.index: 
            # if so append it to results
            results.append(df.loc[(user_id, item_id)]['rating'])
        else:
            # otherwise make the prediction using the neighbours similiarties and append to results
            results.append(pred(df, user_id, item_id, neighbours)) 


    # print("Predictions time: ", (time() - s))


    return results
