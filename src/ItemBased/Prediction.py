# ----------------------------
# Functions used to make a prediciton 
# Given a item and a user 
# ----------------------------

import pandas as pd
import numpy as np


def get_prediction(user, item, item_ratings_df, sim_matrix):
    # extract item from dataframe
    item_1 = item_ratings_df.loc[item_ratings_df['Item'] == item]
    item_1_users = list(item_1['Users'])[0]

    # check if user already rated item
    if user in item_1_users:
        prediction = list(item_1['Ratings'])[0][item_1_users.index(user)]

    else:
        # accumulators for the equation
        a, b = 0, 0

        for index, row in item_ratings_df.iterrows():
            item_2 = row['Item']
            sim = sim_matrix[item - 1][item_2 - 1]

            # neighbourhood check
            if item_2 != item and sim > 0:
                item_2_users = row['Users']

                # check user has rated item_2
                if user in item_2_users:
                    # get users ratings of item_2
                    item_2_user_rating = row['Ratings'][item_2_users.index(user)]     

                    a += sim * item_2_user_rating
                    b += sim
        
        # finish the operations outside of the equation sums
        prediction = 0 if b == 0 else (a/b)

    return prediction


