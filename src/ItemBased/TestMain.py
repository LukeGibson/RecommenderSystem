# -------------------------------
# For a known input
# Checks the similarity matrix creation function 
# Checks the prediction function of a known rating
# Returns true/false for each if they produced expected result
# -------------------------------

import pandas as pd
import numpy as np

from src.ItemBased import Similarity as sim
from src.ItemBased import Prediction as prd

# from import Similarity as sim
# import Prediction as prd


# test data - as it would be in the database
data = {
    'Item': [1,2,3],
    'Users': [[1,2,3],[1,2,3],[2,3]],
    'Ratings': [[1.5,4.5,0.5],[3.5,0.5,4.5],[4.5,1]],
    'Times': [[0,0,0],[0,0,0],[0,0]]
}

# data moved to dataframe
item_ratings_df = pd.DataFrame(data, columns=['Item', 'Users', 'Ratings', 'Times'])

print("\n", "------ Input Dataframe ------", "\n")
print(item_ratings_df)


# sim_matrix generated from dataframe
sim_matrix = sim.get_sim_matrix(item_ratings_df)

print("\n", "------ Item Similarity Matrix ------", "\n")
print(np.array(sim_matrix))


# lines of the test csv [user, item, time]
ratings_to_predict = [
    [1, 1, 0],
    [1, 3, 0]
]

print("\n", "------ Predictions ------", "\n")

# Calculates the predictions
for entry in ratings_to_predict:
    user = int(entry[0])
    item = int(entry[1])
    time = int(entry[2])

    prediction = prd.get_prediction(user, item, item_ratings_df, sim_matrix)
    
    print(user, item, prediction)

#  ------ Input Dataframe ------
#
#    Item      Users    Ratings      Times
# 0     1  [1, 2, 3]  [2, 5, 1]  [0, 0, 0]
# 1     2  [1, 2, 3]  [4, 1, 5]  [0, 0, 0]
# 2     3     [2, 3]     [5, 1]     [0, 0]
#
#  ------ Item Similarity Matrix ------
#
# [[ 1.         -1.          0.98639392]
#  [-1.          1.         -0.98639392]
#  [ 0.98639392 -0.98639392  1.        ]]
#
#  ------ Predictions ------
#
# 1 1 2
# 1 3 2.0


