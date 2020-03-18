import numpy as np
import math
import time
import pandas as pd


# uses the Pearson coefficient to calculate the similarity between 2 users
# user_ratings_dict = {item_id, rating}
def calc_sim_scores(df, u1):
    u1_avg = df.loc[u1]['rating'].mean()
    u1_items = [y for x, y in df.index if x == u1]

    user_subset = [x for x, y in df.index]
    user_subset.remove(u1)

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

        # if count < 5:
        #     print("DB call time:", db_end - db_start)

        # round the equation output to 3 decimal places
        sim_scores.append((u2, a / (b * c)))

    return sim_scores


# calculate the predicted rating for user on item given a neighbourhood of similar users and their simScores
def pred(df, u1, item_id, neighbours):

    u1_avg = df.loc[u1]['rating'].mean()

    a = 0
    b = 0

    for u2, u2_sim in neighbours:
        u2_avg = u1_avg = df.loc[u2]['rating'].mean()
        
        # check u2 has rated that item, if so accumulate the scores
        if (u2, item_id) in df.index:
            a += u2_sim * (df.loc[(u2, item_id)]['rating'] - u2_avg)
            b += u2_sim
    
    if b == 0:
        result = u1_avg
    else:
        result = u1_avg + (a / b)    

    return result


# cur object is cursor for databases
def get_prediction(user_id, item_id, table_nm, cursor):

    # given a userId get a list of (itemId, ratings) they've made
    df = pd.DataFrame(columns=['userID', 'itemID', 'rating', 'time']).set_index(['userID', 'itemID'])
    user_dict = {"userID": [], "itemID": [], "rating": [], "time": []}
    for row in cursor.execute(f'SELECT itemID, rating, time FROM {table_nm} WHERE userID = ?', (user_id,)):
        user_dict["userID"].append(user_id)
        user_dict["itemID"].append(row[0])
        user_dict["rating"].append(row[1])
        user_dict["time"].append(row[2])
    df = df.append(pd.DataFrame.from_dict(user_dict).set_index(['userID', 'itemID']))

    # check user hasn't already rated item
    if (user_id, item_id) in df.index:
        print("User already rated this item!")
        return df.loc[(user_id, item_id)]['rating']
    # database call - given userItems get a list of userId's who also have a rating for at least 1 of the items
    # userID and all the items they've rated, then look to see how of these are one of the items our user has rated
    items_rated = [y for x, y in df.index]
    thresh = 30 if len(items_rated) > 30 else len(items_rated)
    user_item_count = {}
    for row in cursor.execute(f"SELECT userID FROM {table_nm} WHERE itemID IN ({','.join(map(str, items_rated))})"):
        user_item_count[row[0]] = user_item_count.get(row[0], 0) + 1

    user_subset = []
    for x, y in user_item_count.items():
        if y >= thresh:
            user_subset.append(x)
    user_subset.remove(user_id)

    user_dict = {"userID": [], "itemID": [], "rating": [], "time": []}
    for row in cursor.execute(f"SELECT userID, itemID, rating, time FROM {table_nm} WHERE userID IN ({','.join(map(str, user_subset))})"):
        user_dict["userID"].append(row[0])
        user_dict["itemID"].append(row[1])
        user_dict["rating"].append(row[2])
        user_dict["time"].append(row[3])
    df = df.append(pd.DataFrame.from_dict(user_dict).set_index(['userID', 'itemID']))

    sim_scores = calc_sim_scores(df, user_id)
    # select the neighbourhood topN most similar users from the userSubset
    neighbours = []
    topN = 12_000 if len(sim_scores) > 12_000 else len(sim_scores)

    # orders the sim_scores in accending order - then takes the sim_score indexes of the last N elements:
    # N most similar users.
    user_indexs = np.argsort([score[1] for score in sim_scores])[-topN:]

    for index in user_indexs:
        neighbours.append(sim_scores[index])

    result = pred(ratings_dict, item_id, neighbours, cursor)
    return result