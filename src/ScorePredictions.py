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

# path to the validation file
csv_path = "Data/smallValidation.csv" 

# all test ratings to loop through
with open(csv_path) as csv_file:
    lines = csv.DictReader(csv_file, fieldnames=['userID', 'itemID', 'rating', 'time'])
    data_entries = [(i['userID'], i['itemID'], i['rating'], i['time']) for i in lines]


start = time()

# fixed seed to make sample_list constant
random.seed(1) 
# number of users we do validations on (smaller than total so its faster to run)
sample_size = 2_500 
# get the entries to do a vlaidation on
sample_list = random.sample(data_entries, sample_size) 

# initalsie the error lists
true_abs_errors = []
round_abs_errors = []
ceil_abs_errors = []
floor_abs_errors = []

# for each entry in sample_list
for line in tqdm(sample_list):
    user = int(line[0])
    item_list = [int(line[1])]
    rating = float(line[2])

    # make the predictions for that user
    predictions = MakePredictionV2.get_prediction(user, item_list, "User_table", "Item_table", cur) # make prediction for that entry)

    # check predictions list is not empty
    if predictions is not None: 
        # extract the single prediciton
        pred = predictions[0]
        # check the acctaul prediction is not None
        if pred is not None: 
            # calculate the different roundings
            round_05 = round(pred * 2) / 2
            ceil_05 = ceil(pred * 2) / 2
            floor_05 = floor(pred * 2) / 2

            # print(user, item_list)
            # print(f"True Value: {pred}, Rounded pred: {round_05}, Ceil pred: {ceil_05}, Floor pred: {floor_05}")

            # store list of absolute errors
            true_abs_errors.append(abs(pred - rating))
            round_abs_errors.append(abs(round_05 - rating))
            ceil_abs_errors.append(abs(ceil_05 - rating))
            floor_abs_errors.append(abs(floor_05 - rating))


# writing the errors to file
local_dir = str(os.path.dirname(__file__)) + "\\PredErrors\\"

# generate directory
try:
    os.makedirs(local_dir)
except OSError:
    print("Truth Dir Exists")
else:
    print("Truth Dir Created")

true_file = str(local_dir + "trueErrors.txt")
round_file = str(local_dir + "roundErrors.txt")
ceil_file = str(local_dir + "ceilErrors.txt")
floor_file = str(local_dir + "floorErrors.txt")

with open(true_file, 'w') as file:
    for pred in true_abs_errors:
        file.write("%f\n" % pred)

with open(round_file, 'w') as file:
    for pred in round_abs_errors:
        file.write("%f\n" % pred)

with open(ceil_file, 'w') as file:
    for pred in ceil_abs_errors:
        file.write("%f\n" % pred)

with open(floor_file, 'w') as file:
    for pred in floor_abs_errors:
        file.write("%f\n" % pred)

# calulate the squared errors
true_square_errors = [x ** 2 for x in true_abs_errors]
round_square_errors = [x ** 2 for x in round_abs_errors]
floor_square_errors = [x ** 2 for x in floor_abs_errors]
ceil_square_errors = [x ** 2 for x in ceil_abs_errors]

# print the MSE results
print("------- MSE --------")
print(f"Truth = {np.mean(true_square_errors)}")
print(f"Rounding = {np.mean(round_square_errors)}")
print(f"Flooring = {np.mean(floor_square_errors)}")
print(f"Ceiling = {np.mean(ceil_square_errors)}")

# print the MAE results
print("------- MAE --------")
print(f"Truth = {np.mean(true_abs_errors)}")
print(f"Rounding = {np.mean(round_abs_errors)}")
print(f"Flooring = {np.mean(floor_abs_errors)}")
print(f"Ceiling = {np.mean(ceil_abs_errors)}")

print("\n")
print(f"Total time taken: {time() - start}")