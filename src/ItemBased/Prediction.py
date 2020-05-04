# ----------------------------
# Functions used to make a prediciton 
# Given a item and a user 
# ----------------------------

import pandas as pd
import numpy as np
# from time import process_time as time
import time
from tqdm import tqdm

def get_prediction(item_1, data, item_list, all_item_data, sim_matrix, user_avg_ratings):
    # dictionary of user -> rating
    output = {}

    # check item exists 
    if item_1 in item_list:
        # extract item data and index
        item_1_data = all_item_data[item_1]
        item_1_index = item_list.index(item_1)
        item_sim_scores_col = sim_matrix[:item_1_index, item_1_index]
        item_sim_scores_row = sim_matrix[item_1_index, item_1_index:]

        sim_scores = np.concatenate((item_sim_scores_col, item_sim_scores_row))
        scores = zip(sim_scores, item_list)
        scores = [(s, i) for s, i in scores if s > 0]

        # get top n scores
        # scores.sort(reverse = True, key = lambda x: x[0])

        # top_n = 6000
        # if len(scores) > top_n:
        #     scores = scores[:top_n]

        for user in data.keys():
            # check if user has already rated item
            if user in item_1_data.keys():
                output[user] = item_1_data[user]
            else:
                # accumulators for the equation
                a, b = 0, 0

                for score, item_2 in scores:                  
                    # extract item 2 data                     
                    item_2_data = all_item_data[item_2]

                    # check user has rated item_2
                    if user in item_2_data.keys():
                        item_2_user_rating = item_2_data[user]

                        a += score * item_2_user_rating
                        b += score

                # finish the operations outside of the equation sums
                output[user] = 0 if b == 0 else (a/b)
    else:
        for user in data.keys():
            # use the users avaerage rating across other items
            if user in user_avg_ratings.keys():
                rating = user_avg_ratings[user]
            # if they've not rated any items use 2.5
            else:
                rating = 2.5

            output[user] = rating
    
    return output
