import sqlite3
import os
import csv
from matplotlib import pyplot as plt
import seaborn as sns
from time import time
from math import pow, ceil, floor
from tqdm import tqdm
import MakePredictionV2
import random
import numpy as np

# name of .db file to use
name = "validation" 
local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir,  name + '.db')
connection = sqlite3.connect(db_path)
cur = connection.cursor()


csv_path = "Data/smallValidation.csv" # path to the validation file

# all test ratings to loop through
with open(csv_path) as csv_file:
    lines = csv.DictReader(csv_file, fieldnames=['userID', 'itemID', 'rating', 'time'])
    data_entries = [(i['userID'], i['itemID'], i['rating'], i['time']) for i in lines]



start = time()
count = 0 # total count of predictions used to calculate MSE

random.seed(1) # fixed seed to make sample_list constant
sample_size = 2_500 # number of users we do validations on (smaller than total so its faster to run)
sample_list = random.sample(data_entries, sample_size) # get the entries to do a vlaidation on

round_abs_errors = []
ceil_abs_errors = []
floor_abs_errors = []

# for each entry in sample_list
for line in tqdm(sample_list):
    user = int(line[0])
    item_list = [int(line[1])]
    rating = float(line[2])

    # predictions = MakePrediction.get_prediction(user, item_list, "ratings", cur)
    predictions = MakePredictionV2.get_prediction(user, item_list, "User_table", "Item_table", cur) # make prediction for that entry)

    if predictions is not None: # check prediction list is a value
        pred = predictions[0]
        if pred is not None: # check the acctaul prediction is a value (not returned none due to exceeding bounds)
            round_05 = round(pred * 2) / 2
            ceil_05 = ceil(pred * 2) / 2
            floor_05 = floor(pred * 2) / 2

            # print(user, item_list)
            # print(f"True Value: {pred}, Rounded pred: {round_05}, Ceil pred: {ceil_05}, Floor pred: {floor_05}")

            # store list of absolute errors
            round_abs_errors.append(abs(round_05 - rating))
            ceil_abs_errors.append(abs(ceil_05 - rating))
            floor_abs_errors.append(abs(floor_05 - rating))

            count += 1



# writing the errors to file
local_dir = str(os.path.dirname(__file__)) + "\\PredErrors\\"

# generate directory
try:
    os.makedirs(local_dir)
except OSError:
    print("Truth Dir Exists")
else:
    print("Truth Dir Created")


round_file = str(local_dir + "roundErrors.txt")
ceil_file = str(local_dir + "ceilErrors.txt")
floor_file = str(local_dir + "floorErrors.txt")


with open(round_file, 'w') as file:
    for pred in round_abs_errors:
        file.write("%f\n" % pred)

with open(ceil_file, 'w') as file:
    for pred in ceil_abs_errors:
        file.write("%f\n" % pred)

with open(floor_file, 'w') as file:
    for pred in floor_abs_errors:
        file.write("%f\n" % pred)

round_square_errors = [x ** 2 for x in round_abs_errors]
floor_square_errors = [x ** 2 for x in floor_abs_errors]
ceil_square_errors = [x ** 2 for x in ceil_abs_errors]


print("------- MSE --------")
print(f"Rounding = {np.mean(round_square_errors)}")
print(f"Flooring = {np.mean(floor_square_errors)}")
print(f"Ceiling = {np.mean(ceil_square_errors)}")

print("------- MAE --------")
print(f"Rounding = {np.mean(round_abs_errors)}")
print(f"Flooring = {np.mean(floor_abs_errors)}")
print(f"Ceiling = {np.mean(ceil_abs_errors)}")

print("\n")
print(f"Total time taken: {time() - start}")