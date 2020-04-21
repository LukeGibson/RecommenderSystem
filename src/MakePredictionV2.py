import numpy as np
from math import sqrt, pow
from time import time
import pandas as pd


# uses the Pearson coefficient to calculate the similarity between 2 users
def calc_sim_scores(df, u1, user_subset):
    
    u1_avg = df.loc[u1]['rating'].mean() # caclculate average rating for u1
    u1_items = [y for x, y in df.index if x == u1] # all items user 1 rated

    sim_scores = [] # list of (user, simScore) we eventually return

    for u2 in user_subset:
       
        u2_items = [y for x, y in df.index if x == u2] 
        shared_items = [s for s in u1_items if s in u2_items] # get shared items

        # given a userId and the sharedItems return the list of ratings
        u2_avg = df.loc[u2]['rating'].mean()
        # accumulator for 3 parts of sim equation
        a, b, c = 0, 0, 0

        for item in shared_items:
            rating_u1 = df.loc[(u1, item)]['rating'] - u1_avg
            rating_u2 = df.loc[(u2, item)]['rating'] - u2_avg

            a += rating_u1 * rating_u2
            b += pow(rating_u1, 2)
            c += pow(rating_u2, 2)

        b = sqrt(b)
        c = sqrt(c)
        score = 0 if b == 0 or c == 0 else (a/(b*c))
        # score = max(0, min(1, score))
        sim_scores.append((u2, score))

    return sim_scores


# calculate the predicted rating for user on item given a neighbourhood of similar users and their simScores
def pred(df, u1, item_id, neighbours):
    u1_avg = df.loc[u1]['rating'].mean() # calculate u1 average
    
    a, b = 0, 0

    for u2, u2_sim in neighbours:
        u2_avg = df.loc[u2]['rating'].mean() #  calulate u2 average

        if (u2, item_id) in df.index:
            a += u2_sim * (df.loc[(u2, item_id)]['rating'] - u2_avg)
            b += u2_sim

    predict = u1_avg if b == 0 else u1_avg + (a/b)

    # clamps predict within 0 and 5
    # predict = max(0, min(5, predict))

    # Return None, done to see how good the normal predictions are
    if predict > 5 or predict < 0:
        return None
    else:
        return predict


# user_id
# item_list
# user_table_nm = the table where each row is a indevidual rating of an indevidual user
# item_table_nm = table where each row is a item with all the users that rated it
def get_prediction(user_id, item_list, user_table_nm, item_table_nm, cursor):


    # given a userId get a dataframe of all their ratings
    df = pd.DataFrame(columns=['userID', 'itemID', 'rating', 'time']).set_index(['userID', 'itemID'])
    user_dict = {"userID": [], "itemID": [], "rating": [], "time": []}
    s = time()
    for row in cursor.execute(f'SELECT itemID, rating, time FROM {user_table_nm} WHERE userID = ?', (user_id,)):
        user_dict["userID"].append(user_id)
        user_dict["itemID"].append(row[0])
        user_dict["rating"].append(row[1])
        user_dict["time"].append(row[2])
    df = df.append(pd.DataFrame.from_dict(user_dict).set_index(['userID', 'itemID']))
    # print("First DB call", (time() - s))


    s = time()

    # getting building dict of user to number of u1's items they've rates
    items_rated = [y for x, y in df.index] # list of all items u1 rated
    user_item_count = {} # dictionary that counts each user to how many times they've rated an item that u1 rated
    items_to_search = ','.join(map(str, items_rated)) # string format of items rated (joined on commas)

    # go through item table get the user where itemId is one of the items_to_search - incremnt the users count for each item
    for row in cursor.execute(f"SELECT userID FROM {item_table_nm} WHERE itemID IN ({items_to_search})"):
        user_item_count[row[0]] = user_item_count.get(row[0], 0) + 1



    # removing users from dict if count is less then threshold, and removing duplicates
    user_subset = [] # subset of users from above that have rated the most items
    max_user_size = 40 # top n users that have rated the most items

    # order dirctory and select the top n users
    for k, v in sorted(user_item_count.items(), key=lambda item: item[1], reverse=True):
        if len(user_subset) < max_user_size and not k == user_id:
            user_subset.append(k)
    # print("Second DB call", (time() - s))



    # for the reduced users get all of their details
    # both these calls are not needed but make things easier, if need one can go which by having a very,
    # very large pandas dataframe and then having an accompaning list of users who meet the threshold.
    s = time()
    user_dict = {"userID": [], "itemID": [], "rating": [], "time": []}
    for row in cursor.execute(f"SELECT userID, itemID, rating, time FROM {user_table_nm} WHERE userID IN ({','.join(map(str, user_subset))})"):
        user_dict["userID"].append(row[0])
        user_dict["itemID"].append(row[1])
        user_dict["rating"].append(row[2])
        user_dict["time"].append(row[3])
    df = df.append(pd.DataFrame.from_dict(user_dict).set_index(['userID', 'itemID']))
    # print("Third DB call", (time() - s))


    # calculate the similarity scores
    s = time()
    if len(user_subset) == 0: # check the user subset has users  (NEED TO FIGURE OUT WHAT TO DO IN THIS CASE)
        return None

    # takes dataframe of all users ratings
    sim_scores = calc_sim_scores(df, user_id, user_subset)

    pos_sim_scores = [x for x in sim_scores if x[1] > 0] # filters returned simScores to only show positive 
    # print("Sim time: ", (time() - s))

    # get index of topN users, based on sim score
    s = time()
    neighbours = [] # sorted list of simScores
    topN = 12_000 if len(pos_sim_scores) > 12_000 else len(pos_sim_scores)
    user_indexes = np.argsort([score[1] for score in pos_sim_scores])[-topN:]
    for index in user_indexes:
        neighbours.append(pos_sim_scores[index])

    results = [] # the final list opf predictions (in the order of input parameter of items)
    for item_id in item_list:
        if (user_id, item_id) in df.index: 
            results.append(df.loc[(user_id, item_id)]['rating']) # User already rated this item so just return it
        else:
            results.append(pred(df, user_id, item_id, neighbours)) # Otherwise make the prediction using the neighbours similiarties
    # print("Predictions time: ", (time() - s))
    return results
