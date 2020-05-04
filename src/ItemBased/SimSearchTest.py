import pandas as pd
import numpy as np

# sim_matrix = np.array([
#     [0,1,1,1,3,1,1,1],
#     [0,0,1,1,3,1,1,1],
#     [0,0,0,1,3,1,1,1],
#     [0,0,0,0,3,1,1,1],
#     [0,0,0,0,0,2,2,2],
#     [0,0,0,0,0,0,1,1],
#     [0,0,0,0,0,0,0,1],
#     [0,0,0,0,0,0,0,0]
# ])

# item_1_index = 4
# item_sim_scores_col = sim_matrix[:item_1_index, item_1_index]
# item_sim_scores_row = sim_matrix[item_1_index, item_1_index + 1:]

# total = np.concatenate((item_sim_scores_col, item_sim_scores_row))

# print(item_sim_scores_col)
# print(item_sim_scores_row)
# print(total)


scores = [(1.4,6),(0.4,9),(55,5),(43,1)]

print(scores)

scores.sort(reverse = True, key = lambda x: x[0])

print(scores)


top_n = 4
if len(scores) > top_n:
    scores = scores[:top_n]

print(scores)