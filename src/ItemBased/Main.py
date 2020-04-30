# -------------------------------
# Given a database, similarity matrix and test csv
# Create item data dictionary
# Read the similarity matrix
# Read test csv
# Calculate the predicted ratings in the test csv
# Write the preditions to a file
# -------------------------------

import os
import sqlite3
import csv
import pandas as pd
import numpy as np
from tqdm import tqdm
from time import process_time as time

import Prediction as prd


# Name cvs file for predictions to make
db_name = "small"
table_name = "Ratings"
test_csv_name = "comp3208-test-small"


# Create item data dictionary
start_time = time()

local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir, "..", "..", "Data", "Databases", db_name + ".db")
connection = sqlite3.connect(db_path)
cur = connection.cursor()

items = []
for row in cur.execute(f"SELECT DISTINCT(ItemID) FROM {table_name}"):
    items.append(row[0])
num_items = len(items)

all_item_data = {}
for i in tqdm(range(num_items)):
    item = items[i]
    item_data = {}
    for row in cur.execute(f"SELECT UserID, Rating FROM {table_name} WHERE ItemID = {item}"):
        item_data[row[0]] = row[1]
    all_item_data[item] = item_data
print("> Built item data dictionary of size:", len(all_item_data))


# Load similarity matrix
sim_matrix_path = os.path.join(local_dir, "..", "..", "Data", "Output", "sim-matrix-" + db_name + ".npy")
sim_matrix = np.load(sim_matrix_path)

print("> Loaded similarity matrix of size:", sim_matrix.shape)


# Get list of (user, item, time) predictions to make
test_csv_path = os.path.join(local_dir, "..", "..", "Data", "CSV", test_csv_name + ".csv")

with open(test_csv_path) as csv_file:
    lines = csv.DictReader(csv_file, fieldnames=['userID', 'itemID', 'time'])
    ratings_to_predict = [(i['userID'], i['itemID'], i['time']) for i in lines]


# dict: item - dict: user - time


# Generate predictions
predictions = []

for entry in (ratings_to_predict):
    user = int(entry[0])
    item = int(entry[1])
    time = int(entry[2])

    prediction = prd.get_prediction(user, item, items, all_item_data, sim_matrix)
    # print("user", user, "item", item, ": rating", prediction)
    predictions.append((user, item, prediction))


# Write predictions csv file
predictions_path = os.path.join(local_dir, "..", "..", "Data", "Output", "predictions-" + db_name + ".csv")

with open(predictions_path,'w', newline='') as results:
    csv_results = csv.writer(results)
    for entry in predictions:
        csv_results.writerow(entry)