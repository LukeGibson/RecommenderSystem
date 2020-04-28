import pandas as pd
import os
import csv
import sqlite3
from src import MakePredictionV2  # using v2 as that uses the item to user table as well as user to item table
from tqdm import tqdm
import numpy as np

local_dir = os.path.dirname(__file__)
size = "small"
csv_path = os.path.join(local_dir, '../Data/comp3208-test-' + size + '.csv')

name = "UserItemTables"
local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir,  name + '.db')
connection = sqlite3.connect(db_path)
cur = connection.cursor()

print("> Reading .CSV file")
with open(csv_path) as input_csv:
    lines = csv.DictReader(input_csv, fieldnames=['userID', 'itemID', 'time'])
    data_entries = [(i['userID'], i['itemID'], i['time']) for i in lines]

print("> Making Input Dictionary")
input_dict = {}

for line in data_entries:
    user = line[0]
    item = line[1]
    if user in input_dict:
        input_dict[user].append(item)
    else:
        input_dict[user] = [item]


output_dict = {}
print("> Calculating user predictions")
for user, items in tqdm(input_dict.items()):
    predictions = MakePredictionV2.get_prediction(user, items, "User_table", "Item_table", cur)
    output_dict[user] = predictions


# # output the df's to csv files
# trainPath = os.path.join(local_dir, "../Data/" + size + "Train.csv")
# valPath = os.path.join(local_dir, "../Data/" + size + "Validation.csv")
# train_df.to_csv(trainPath, index=True, header=False)
# test_df.to_csv(valPath, index=True, header=False)
