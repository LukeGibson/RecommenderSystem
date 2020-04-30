# ----------------------------
# Functions used to make a prediciton 
# Given a item and a user 
# ----------------------------

import pandas as pd
import numpy as np
from time import process_time as time

# complexity: 2n + m + nm 
# n: num of items (19807)
# m: num of ratings for item (0-90000)
def get_prediction(user, item_1, items, all_item_data, sim_matrix):
    start_time = time()

    # check item exists 
    if item_1 in items:                                             # n
        # extract item data and index
        item_1_data = all_item_data[item_1]                         # 1
        item_1_index = items.index(item_1)                          # n
        
        # check if user has already rated item
        if user in item_1_data:                                     # m
            prediction = item_1_data[user]                          # 1
        else:
            # accumulators for the equation
            a, b = 0, 0

            for item_2_index in range(len(items)):                  # n 
                # extract item 2 data
                item_2 = items[item_2_index]                        # 1
                item_2_data = all_item_data[item_2]                 # 1

                # find items similarity
                sim = sim_matrix[item_2_index][item_1_index]        # 1

                # rectrict neighbourhood
                if item_2 != item_1 and sim > 0:                    # 1

                    # check user has rated item_2
                    if user in item_2_data:                         # m
                        item_2_user_rating = item_2_data[user]      # 1

                        a += sim * item_2_user_rating    
                        b += sim
            
            # finish the operations outside of the equation sums
            prediction = 0 if b == 0 else (a/b)
    else:
        prediction = 2.5
    
    print("Prediction time:", time() - start_time)
    return prediction