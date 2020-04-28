# ----------------------------
# Functions used to make the similarity matrix 
# Given a database returns a item similarity matrix
# ----------------------------

import pandas as pd
import numpy as np
from math import sqrt, pow
from statistics import mean
import sqlite3
import os
import numpy as np
from tqdm import tqdm


# trying to make this file as independant as possible so only need the db name and table name
def build_sim_matrix(db_name, table_name):
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
    sim_matrix = np.empty(matrix_shape)
    print(f"> Matrix of dimensions {sim_matrix.shape} made")

    item_avgs = {}
    for row in cur.execute(f"SELECT ItemID, AVG(rating) FROM {table_name} GROUP BY ItemID"):
        item_avgs[row[0]] = row[1]
    print("> Calculated item averages")

    all_item_data = {}
    for i in tqdm(range(num_items)):
        item = items[i]
        item_data = []
        for row in cur.execute(f"SELECT UserID, Rating FROM {table_name} WHERE ItemID = {item}"):
            item_data.append((row[0], row[1]))
        all_item_data[item] = item_data
    print("> Built dictionary of all items data")

    for i in tqdm(range(num_items)):
        item_1 = items[i]
        item_1_avg = item_avgs[item_1]
        # (UserID, Rating) pairs
        item_1_data = all_item_data[item_1]

        for j in range(i + 1, num_items):
            item_2 = items[j]
            item_2_avg = item_avgs[item_2]
            item_2_data = all_item_data[item_2]
            if item_2 <= item_1:
                print(f"Error with calculating sim score for: {item_1} and {item_2}")
            # print(f"Calc for items {item_1} and {item_2}")

            sim_matrix[i][j] = calc_sim(item_1_data, item_2_data, item_1_avg, item_2_avg)

    return sim_matrix
    #
    # # get the number of items in the dataframe
    # num_items = len(item_ratings_df.index)
    #
    # # initalise a (num_items X num_items) sized matrix to store item similarity
    # sim_matrix = [[0 for x in range(num_items)] for y in range(num_items)]
    #
    # # calculate the similarity score for each item
    # for index_1, row_1 in item_ratings_df.iterrows():
    #     for index_2, row_2 in item_ratings_df.iterrows():
    #
    #         # represents the co-ordinates in the sim matrix
    #         item_id_1 = row_1['Item']
    #         item_id_2 = row_2['Item']
    #
    #         # check items are not the same before calulating their sim
    #         if item_id_1 == item_id_2:
    #             item_sim = 1
    #         else:
    #             item_sim = calc_sim(row_1, row_2)
    #
    #         sim_matrix[item_id_1 - 1][item_id_2 - 1] = item_sim
    #
    # return sim_matrix


def calc_sim(item_1_data, item_2_data, item_1_avg, item_2_avg):
    item_1_users = [u for u, r in item_1_data]
    item_2_users = [u for u, r in item_2_data]
    item_1_ratings = [r for u, r in item_1_data]
    item_2_ratings = [r for u, r in item_2_data]

    # find the users that rated both items and the rating they gave
    users_shared = [u for u in item_1_users if u in item_2_users]

    # if no users have rated both items set similarity to 0
    if len(users_shared) == 0:
        sim = 0
    else:
        # perform pearson coefficent calculation
        a, b, c = 0, 0, 0

        for user in users_shared:
            # calculate the items adjusted rating from user
            item_1_rating_adjust = item_1_ratings[item_1_users.index(user)] - item_1_avg
            item_2_rating_adjust = item_2_ratings[item_2_users.index(user)] - item_2_avg
            
            # accumulate the seperate sums of the person coefficent
            a += (item_1_rating_adjust * item_2_rating_adjust)
            b += pow(item_1_rating_adjust, 2)
            c += pow(item_2_rating_adjust, 2)

        # finish the operations outside of the equation sums
        b = sqrt(b)
        c = sqrt(c)

        sim = 0 if b == 0 or c == 0 else (a/(b*c))

    return sim
