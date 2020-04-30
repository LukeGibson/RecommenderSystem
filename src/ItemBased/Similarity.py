# ----------------------------
# Functions used to make the similarity matrix 
# Given a database returns a item similarity matrix
# ----------------------------

import numpy as np
import sqlite3
import os
from tqdm import tqdm
from math import sqrt, pow
from time import process_time as time


# trying to make this file as independant as possible so only need the db name and table name
def build_sim_matrix(db_name, table_name):
    start_time = time()
    # connect to db
    local_dir = os.path.dirname(__file__)
    db_path = os.path.join(local_dir, "..", "..", "Data", "Databases", db_name + ".db")
    connection = sqlite3.connect(db_path)
    cur = connection.cursor()

    items = []
    for row in cur.execute(f"SELECT DISTINCT(ItemID) FROM {table_name}"):
        items.append(row[0])
    num_items = len(items)
    print("> Item list made")

    matrix_shape = (num_items, num_items)
    sim_matrix = np.zeros(matrix_shape, dtype=np.float32)
    print(f"> Matrix of dimensions {sim_matrix.shape} made")

    user_avgs = {}
    for row in cur.execute(f"SELECT UserID, AVG(rating) FROM {table_name} GROUP BY UserID"):
        user_avgs[row[0]] = row[1]
    print("> Calculated user averages")

    all_item_data = {}
    for i in tqdm(range(num_items)):
        item = items[i]
        item_data = {}
        for row in cur.execute(f"SELECT UserID, Rating FROM {table_name} WHERE ItemID = {item}"):
            item_data[row[0]] = row[1]
        all_item_data[item] = item_data
    print("> Built dictionary of all items data")
    # print(all_item_data[3])

    for i in tqdm(range(num_items)):
        item_1 = items[i]
        # (UserID, Rating) pairs
        item_1_data = all_item_data[item_1]

        for j in range(i + 1, num_items):
            item_2 = items[j]
            item_2_data = all_item_data[item_2]
            if item_2 <= item_1:
                print(f"Error with calculating sim score for: {item_1} and {item_2}")
            # print(f"Calc for items {item_1} and {item_2}")

            sim_matrix[i][j] = calc_sim(item_1_data, item_2_data, user_avgs)

    print(sim_matrix)
    np.save('SimMat', sim_matrix)

    print(f"Matrix made, time taken: {time() - start_time}")

    return sim_matrix


def calc_sim(item_1_data, item_2_data, user_avgs):
    # triple of (user, rating for item 1, rating for item 2)
    set_1 = set(item_1_data)
    set_2 = set(item_2_data)
    common_users = set_1.intersection(set_2)

    user_ratings = []
    for u in common_users:
        r1 = item_1_data[u]
        r2 = item_2_data[u]
        user_ratings.append((u, r1, r2))


    # if no users have rated both items set similarity to 0
    if len(user_ratings) == 0:
        return 0
    # perform pearson coefficent calculation
    a, b, c = 0, 0, 0

    for u, r1, r2 in user_ratings:
        user_avg_rating = user_avgs[u]
        # calculate the items adjusted rating from user
        item_1_rating_adjust = r1 - user_avg_rating
        item_2_rating_adjust = r2 - user_avg_rating

        # accumulate the seperate sums of the person coefficent
        a += (item_1_rating_adjust * item_2_rating_adjust)
        b += pow(item_1_rating_adjust, 2)
        c += pow(item_2_rating_adjust, 2)

    # finish the operations outside of the equation sums
    b = sqrt(b)
    c = sqrt(c)

    sim = 0 if b == 0 or c == 0 else (a/(b*c))

    return sim
