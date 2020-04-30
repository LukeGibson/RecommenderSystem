# ----------------------------
# Functions used to make a prediciton 
# Given a item and a user 
# ----------------------------

import pandas as pd
import numpy as np
from time import process_time as time
from tqdm import tqdm

# complexity: 2n + m + nm 
# n: num of items (19807)
# m: num of ratings for item (0-90000)
def get_prediction(item_1, data, item_list, all_item_data, sim_matrix):
    start_time = time()

    # dictionary of user -> rating
    output = {}

    # check item exists 
    if item_1 in item_list:                                             # n
        # extract item data and index
        item_1_data = all_item_data[item_1]                         # 1
        item_1_index = item_list.index(item_1)
        item_sim_scores = sim_matrix[:, item_1_index]

        pos_items = []
        for i in range(len(item_list)):
            score = item_sim_scores[i]
            item = item_list[i]
            if item_sim_scores[i] > 0 and item != item_1:
                pos_items.append((item_list[i], score))

        for user in data.keys():
            # check if user has already rated item
            if user in item_1_data.keys():
                output[user] = item_1_data[user]
            else:
                s = time()
                # accumulators for the equation
                a, b = 0, 0

                for item_2, score in pos_items:                  # n
                    # extract item 2 data                     # 1
                    item_2_data = all_item_data[item_2]

                    # check user has rated item_2
                    if user in item_2_data.keys():                         # m
                        item_2_user_rating = item_2_data[user]      # 1

                        a += score * item_2_user_rating
                        b += score


                # finish the operations outside of the equation sums
                output[user] = 0 if b == 0 else (a/b)
                #print(f"Time: {time() - s}")
    else:
        output = dict.fromkeys(data, 2.5)
    
    # print("Prediction time:", time() - start_time)
    return output
                
            





