import sqlite3
import os
from collections import defaultdict
import numpy as np
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
        score = 0 if b == 0 or c == 0 else (a / (b * c))

        # add the calulated simScore for u2 to returning list
        sim_scores.append((u2, score))

    return sim_scores


def main():
    db_name = "UserItemTables"
    table_name = "User_table"
    local_dir = os.path.dirname(__file__)
    db_path = os.path.join(local_dir, "..", "Data", "Databases", db_name + '.db')
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    user_list = []
    item_dict = defaultdict(list)
    for row in cur.execute(f"SELECT userID, itemID FROM User_table"):
        user_list.append(row[0])
        item_dict.setdefault(row[1], []).append(row[0])
    user_list = list(dict.fromkeys(user_list))
    print("> Built item_dict and user_list")

    scores_per_user = 30
    matrix_shape = (len(user_list), scores_per_user)
    matrix_scores = np.empty(matrix_shape)
    matrix_user = np.empty(matrix_shape)

    print(f"Len of user list: {len(user_list)}")

    for user in user_list:
        # rem_users = user_list[user_list.index(user) + 1:]
        df = pd.DataFrame(columns=['userID', 'itemID', 'rating', 'time']).set_index(['userID', 'itemID'])
        user_dict = {"userID": [], "itemID": [], "rating": [], "time": []}

        for row in cursor.execute(f'SELECT itemID, rating, time FROM {table_name} WHERE userID = {user}'):
            user_dict["userID"].append(user)
            user_dict["itemID"].append(row[0])
            user_dict["rating"].append(row[1])
            user_dict["time"].append(row[2])
        df = df.append(pd.DataFrame.from_dict(user_dict).set_index(['userID', 'itemID']))








main()
