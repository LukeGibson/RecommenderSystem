import numpy as np
import math
from time import time
import pandas as pd


# uses the Pearson coefficient to calculate the similarity between 2 users
def calc_sim_scores(df, u1, user_subset):

    u1_avg = df.loc[u1]['rating'].mean()
    u1_items = [y for x, y in df.index if x == u1]

    sim_scores = []

    for u2 in user_subset:
        # get shared items
        u2_items = [y for x,y in df.index if x == u2]
        shared_items = [s for s in u1_items if s in u2_items]

        # given a userId and the sharedItems return the list of ratings

        u2_avg = df.loc[u2]['rating'].mean()
        # accumulator for 3 parts of sim equation
        a, b, c = 0, 0, 0

        for item in shared_items:
            rating_u1 = df.loc[(u1, item)]['rating'] - u1_avg
            rating_u2 = df.loc[(u2, item)]['rating'] - u2_avg

            rating_u1_sq = rating_u1 * rating_u1
            rating_u2_sq = rating_u2 * rating_u2

            a += rating_u1 * rating_u2
            b += rating_u1_sq
            c += rating_u2_sq

        b = math.sqrt(b)
        c = math.sqrt(c)

        sim_scores.append((u2, a / (b * c)))

    return sim_scores


# calculate the predicted rating for user on item given a neighbourhood of similar users and their simScores
def pred(df, u1, item_id, neighbours):
    u1_avg = df.loc[u1]['rating'].mean()
    a, b = 0, 0

    for u2, u2_sim in neighbours:
        u2_avg = df.loc[u2]['rating'].mean()

        if (u2, item_id) in df.index:
            a += u2_sim * (df.loc[(u2, item_id)]['rating'] - u2_avg)
            b += u2_sim

    return u1_avg if b == 0 else u1_avg + (a/b)


# cur object is cursor for databases
def get_prediction(user_id, item_list, table_nm, cursor):

    # given a userId get a list of (itemId, ratings) they've made
    df = pd.DataFrame(columns=['userID', 'itemID', 'rating', 'time']).set_index(['userID', 'itemID'])
    user_dict = {"userID": [], "itemID": [], "rating": [], "time": []}
    s = time()
    for row in cursor.execute(f'SELECT itemID, rating, time FROM {table_nm} WHERE userID = ?', (user_id,)):
        user_dict["userID"].append(user_id)
        user_dict["itemID"].append(row[0])
        user_dict["rating"].append(row[1])
        user_dict["time"].append(row[2])
    df = df.append(pd.DataFrame.from_dict(user_dict).set_index(['userID', 'itemID']))
    print("First DB call", (time() - s))
    # getting building dict of user to number of u1's items they've rates
    items_rated = [y for x, y in df.index]
    thresh = 30 if len(items_rated) > 30 else len(items_rated)
    user_item_count = {}
    items_to_search = ','.join(map(str, items_rated))
    s = time()
    for row in cursor.execute(f"SELECT userID FROM {table_nm} WHERE itemID IN ({items_to_search})"):
        user_item_count[row[0]] = user_item_count.get(row[0], 0) + 1
    print("Second DB call", (time() - s))
    # removing users from dict if count is less then threshold, and removing duplicates
    user_subset = []
    for x, y in user_item_count.items():
        if y >= thresh and x not in user_subset:
            user_subset.append(x)
    user_subset.remove(user_id)

    # for the reduced users get all of their details
    # both these calls are not needed but make things easier, if need one can go which by having a very,
    # very large pandas dataframe and then having an accompaning list of users who meet the threshold.
    s = time()
    user_dict = {"userID": [], "itemID": [], "rating": [], "time": []}
    for row in cursor.execute(f"SELECT userID, itemID, rating, time FROM {table_nm} WHERE userID IN ({','.join(map(str, user_subset))})"):
        user_dict["userID"].append(row[0])
        user_dict["itemID"].append(row[1])
        user_dict["rating"].append(row[2])
        user_dict["time"].append(row[3])
    df = df.append(pd.DataFrame.from_dict(user_dict).set_index(['userID', 'itemID']))
    print("Third DB call", (time() - s))

    sim_scores = calc_sim_scores(df, user_id, user_subset)

    # get index of topN users, based on sim score
    neighbours = []
    topN = 12_000 if len(sim_scores) > 12_000 else len(sim_scores)
    user_indexes = np.argsort([score[1] for score in sim_scores])[-topN:]
    for index in user_indexes:
        neighbours.append(sim_scores[index])

    results = []
    for item_id in item_list:
        if (user_id, item_id) in df.index:
            # User already rated this item so just return it
            results.append(df.loc[(user_id, item_id)]['rating'])
        else:
            results.append(pred(df, user_id, item_id, neighbours))
    return results
