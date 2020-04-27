# ----------------------------
# Functions used to make the similarity matrix 
# Given a database returns a item similarity matrix
# ----------------------------

import pandas as pd
import numpy as np
from math import sqrt, pow
from statistics import mean


def get_sim_matrix(item_ratings_df):
    # get the number of items in the dataframe
    num_items = len(item_ratings_df.index)

    # initalise a (num_items X num_items) sized matrix to store item similarity
    sim_matrix = [[0 for x in range(num_items)] for y in range(num_items)]
    
    # calculate the similarity score for each item
    for index_1, row_1 in item_ratings_df.iterrows():
        for index_2, row_2 in item_ratings_df.iterrows():

            # represents the co-ordinates in the sim matrix
            item_id_1 = row_1['Item']
            item_id_2 = row_2['Item']

            # check items are not the same before calulating their sim
            if item_id_1 == item_id_2:
                item_sim = 1
            else:
                item_sim = calc_sim(row_1, row_2)

            sim_matrix[item_id_1 - 1][item_id_2 - 1] = item_sim

    return sim_matrix



# takes the dataframe rows of 2 items
def calc_sim(row_1, row_2):
    item_1_users = row_1['Users']
    item_2_users = row_2['Users']
    item_1_ratings = row_1['Ratings']
    item_2_ratings = row_2['Ratings']

    # calculate average ratings for both items
    item_1_rating_avg = mean(item_1_ratings)
    item_2_rating_avg = mean(item_2_ratings)

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
            item_1_rating_adjust = item_1_ratings[item_1_users.index(user)] - item_1_rating_avg
            item_2_rating_adjust = item_2_ratings[item_2_users.index(user)] - item_2_rating_avg
            
            # accumulate the seperate sums of the person coefficent
            a += (item_1_rating_adjust * item_2_rating_adjust)
            b += pow(item_1_rating_adjust, 2)
            c += pow(item_2_rating_adjust, 2)

        # finish the operations outside of the equation sums
        b = sqrt(b)
        c = sqrt(c)

        sim = 0 if b == 0 or c == 0 else (a/(b*c))

    return sim
     
