# file for looking at how long predictions take to run, not accuracy

import sqlite3
import os
from time import time
from src import MakePrediction, MakePredictionPandas, MakePredictionV2

name = "ratings"
local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir,  name + '.db')
connection = sqlite3.connect(db_path)
cur = connection.cursor()


# Tests

# start = time()
# for i in range(10):
#     r = MakePrediction.get_prediction(1, 3, "ratings", cur)
#     print(f"Made prediction: {i + 1} of {r}")
# end = time()
# avg_time = (end - start)/10
# small_predictions = 496526
# print(f"Time for, on average, per prediction = {round(avg_time, 4)} seconds")
# print(f"Time for all small test predictions = {(avg_time * small_predictions) / 3600} hrs")

start = time()
item_list = [17460, 12041, 2488, 18337, 4170, 3886, 18781, 844, 16183, 13940, 416, 8902, 2184, 16784, 16544]
print(f"Making {len(item_list)} predictions")
ratings = MakePredictionPandas.get_prediction(1, item_list, "ratings", cur)
print(f"Made {len(ratings)} predictions")
end = time()
avg_time = (end - start)/len(item_list)
small_predictions = 496526 / len(item_list)
print(f"Time for, on average, per prediction = {round(avg_time, 4)} seconds")
print(f"Time for all small test predictions = {(avg_time * small_predictions) / 3600} hrs")

# Run 1, with no optimizations on 17/03 - still having about 4 db calls
# Time for, on average, per prediction = 5.9341 seconds
# Time for all small test predictions = 818.4489972975651 hrs
# Run 2, using pandas dataframe
# needs checking
# Run 3, predicting multiple items at once
# Time for, on average, per prediction = 0.4197 seconds
# Time for all small test predictions = 3.8589181030385284 hrs


# from src import MakePredictionV2
# name = "ratingsV2"
# local_dir = os.path.dirname(__file__)
# db_path = os.path.join(local_dir,  name + '.db')
# connection = sqlite3.connect(db_path)
# cur = connection.cursor()
#
#
# # Tests
# u = 1
# i = 3
# r = MakePredictionV2.get_prediction(u, i, "ratings_main", cur)
# print("user", u, "for item", i, "has predicted rating", r)