# get list of all users
# build numpy array of users x users
# nested for loop that goes through each possible pairing and adds it too the matrix
# find a way to write and read the numpy array to system
# find a way of getting the n highest sim scores for a users and returning the respective users
# look at how this can be intergrated into the makeprediction files
import sqlite3
import os
import numpy as np
import pandas as pd
from math import sqrt
from time import time
from tqdm import tqdm

name = "validation"
local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir,  name + '.db')
connection = sqlite3.connect(db_path)
cursor = connection.cursor()
table_nm = "ratings"


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

        b = sqrt(b)
        c = sqrt(c)
        if b == 0 or c == 0:
            sim_scores.append((u2, 0))
        else:
            sim_scores.append((u2, a / (b * c)))

    return sim_scores


user_ids = []
for row in cursor.execute(f'SELECT DISTINCT userID FROM {table_nm}'):
    user_ids.append(row[0])

# going to have two np matrices, one for the scores and one for the users that the score relates to
# as there are a large number of users, we only use select the x users who have rated the most items
n = len(user_ids)
x = 50
user_matrix = np.zeros(shape=(n, x), dtype=np.int)
scores_matrix = np.zeros(shape=(n, x), dtype=np.float)

# to make sure scores are calculated twice
users_calculated = []
for i in tqdm(range(n)):
    u1 = user_ids[i]
    users_calculated.append(u1)

    df = pd.DataFrame(columns=['userID', 'itemID', 'rating']).set_index(['userID', 'itemID'])
    user_dict = {"userID": [], "itemID": [], "rating": []}
    s = time()
    for row in cursor.execute(f'SELECT itemID, rating FROM {table_nm} WHERE userID = ?', (u1,)):
        user_dict["userID"].append(u1)
        user_dict["itemID"].append(row[0])
        user_dict["rating"].append(row[1])
    df = df.append(pd.DataFrame.from_dict(user_dict).set_index(['userID', 'itemID']))

    # reduce this down to get the top 50
    u2s = user_ids[i + 1:]

    # count the number of times the others users have rated u1 items
    items_rated = [y for x, y in df.index]
    user_item_count = {}
    items_to_search = ','.join(map(str, items_rated))
    s = time()
    for row in cursor.execute(f"SELECT userID FROM {table_nm} WHERE itemID IN ({items_to_search})"):
        user_item_count[row[0]] = user_item_count.get(row[0], 0) + 1
    # print("Second DB call", (time() - s))

    # take the top x users from user_item_count
    user_subset = []
    for k, v in sorted(user_item_count.items(), key=lambda item: item[1], reverse=True):
        if len(user_subset) >= x:
            break
        if not k == u1:
            user_subset.append(k)

    user_dict = {"userID": [], "itemID": [], "rating": []}
    for row in cursor.execute(
            f"SELECT userID, itemID, rating FROM {table_nm} WHERE userID IN ({','.join(map(str, user_subset))})"):
        user_dict["userID"].append(row[0])
        user_dict["itemID"].append(row[1])
        user_dict["rating"].append(row[2])
    df = df.append(pd.DataFrame.from_dict(user_dict).set_index(['userID', 'itemID']))

    sim_scores = calc_sim_scores(df, u1, user_subset)
    for j in range(len(sim_scores)):
        user_matrix[i, j] = sim_scores[j][0]
        scores_matrix[i, j] = sim_scores[j][1]
