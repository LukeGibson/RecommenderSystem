import sqlite3
import os
from collections import defaultdict, Counter
import numpy as np
import pandas as pd
from tqdm import tqdm
from math import sqrt
from time import time
import itertools


# uses the pearson coefficient to calculate the similarity between 2 users
def calc_sim_scores(df, u1, user_subset, user_avgs):
    # average rating for u1
    if user_avgs[u1] == -1:
        user_avgs[u1] = df.loc[u1]['rating'].mean()
    u1_avg = user_avgs[u1]

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
        if user_avgs[u2] == -1:
            user_avgs[u2] = df.loc[u2]['rating'].mean()
        u2_avg = user_avgs[u2]

        # accumulator for 3 parts of sim equation
        a, b, c = 0, 0, 0

        # loop through each of the items u1 and u2 rated
        for item in shared_items:
            # calculate the difference from their average rating
            rating_u1 = df.loc[(u1, item)]['rating'] - u1_avg
            rating_u2 = df.loc[(u2, item)]['rating'] - u2_avg

            # accumulate the separate sums of the sim equation
            a += (rating_u1 * rating_u2)
            b += pow(rating_u1, 2)
            c += pow(rating_u2, 2)

        # finish the operations outside of the sim equation sums
        b = sqrt(b)
        c = sqrt(c)

        # check for divide by 0 error
        score = 0 if b == 0 or c == 0 else (a / (b * c))

        # add the calculated simScore for u2 to returning list
        sim_scores.append((u2, score))

    return sim_scores

# need to try and make this function like 50x faster
def get_top_users(user, df, item_dict):
    # list of all items u1 rated
    items_rated = [y for x, y in df.index]
    user_list = []
    s = time()
    for item in items_rated:
        user_list += item_dict[item]
    #print(f"Concat = {time() - s}")

    s = time()
    user_list = list(filter(user.__ne__, user_list))
    #print(f"Filtering = {time() - s}")

    s = time()
    user_subset = [k for k, v in Counter(user_list).most_common(30)]
    #print(f"Counting = {time() - s}")
    #print()
    # print(user_subset)

    return user_subset

def main():
    db_name = "UserItemTables"
    user_table_name = "User_table"
    item_table_name = "Item_table"
    local_dir = os.path.dirname(__file__)
    db_path = os.path.join(local_dir, "..", "Data", "Databases", db_name + '.db')
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    user_list = []
    item_dict = defaultdict(list)
    for row in cursor.execute(f"SELECT userID, itemID FROM {user_table_name}"):
        user_list.append(row[0])
        #item_dict.setdefault(row[1], []).append(row[0])
    user_list = list(dict.fromkeys(user_list))
    print(len(user_list))
    print("> Built item_dict and user_list")

    scores_per_user = 30
    matrix_shape = (len(user_list), scores_per_user)
    matrix_scores = np.empty(matrix_shape)
    matrix_user = np.empty(matrix_shape)

    user_avg_ratings = dict.fromkeys(user_list, -1)

    # print(f"Len of user list: {len(user_list)}")

    for i in range(len(user_list)): #tqdm(user_list):
        user = user_list[i]
        s1 = time()
        # rem_users = user_list[user_list.index(user) + 1:]
        s = time()
        df = pd.DataFrame(columns=['userID', 'itemID', 'rating', 'time']).set_index(['userID', 'itemID'])
        user_dict = {"userID": [], "itemID": [], "rating": [], "time": []}

        for row in cursor.execute(f'SELECT itemID, rating, time FROM {user_table_name} WHERE userID = {user}'):
            user_dict["userID"].append(user)
            user_dict["itemID"].append(row[0])
            user_dict["rating"].append(row[1])
            user_dict["time"].append(row[2])
        df = df.append(pd.DataFrame.from_dict(user_dict).set_index(['userID', 'itemID']))
        print(f"1st DB call: {time() - s}")

        s = time()
        items_rated = [y for x, y in df.index]
        items_to_search = ','.join(map(str, items_rated))
        top_users = []
        for row in cursor.execute(
                f'SELECT UserID, COUNT(UserID) AS User_Count FROM {item_table_name} ' +
                f'WHERE ItemID IN ({items_to_search}) GROUP BY UserID ORDER BY User_Count DESC'):
            # user_item_count[row[0]] = row[1]
            if len(top_users) > 30:
                break
            u2 = row[0]
            if not u2 == user:
                top_users.append(row[0])

        print(f"2nd DB call: {time() - s}")
        #
        # if len(user_subset) == 0:
        #     print(f"Ah problem with user {user}")
        #
        # # check if any of user subset < user
        # smaller_users = [u for u in user_subset if u < user]
        # # for these values check if sim score already calculated
        # for s in smaller_users:
        #     idx = user_list.index(s)
        #     if s in matrix_user[idx]:
        #         print(matrix_user[idx])
        #         print(matrix_scores[idx])
        #         user_subset.remove(s)
        # # print(smaller_user)
        #
        # # print(f"Total time: {time() - s1}")
        #
        s = time()
        # append to df with the remaining users
        user_dict = {"userID": [], "itemID": [], "rating": [], "time": []}
        for row in cursor.execute(
                f"SELECT userID, itemID, rating, time FROM {user_table_name} WHERE userID IN ({','.join(map(str, top_users))})"):
            user_dict["userID"].append(row[0])
            user_dict["itemID"].append(row[1])
            user_dict["rating"].append(row[2])
            user_dict["time"].append(row[3])
        df = df.append(pd.DataFrame.from_dict(user_dict).set_index(['userID', 'itemID']))
        print(f"3rd DB call: {time() - s}")
        print()
        #
        # sim_scores = calc_sim_scores(df, user, user_subset, user_avg_ratings)
        # matrix_user[i, :] = [x for x, y in sim_scores]
        # matrix_scores[i, :] = [y for x, y in sim_scores]

        # add sim scores to matrix and users to second matrix at same positions








main()
