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
from datetime import datetime
import Prediction as prd


# Name cvs file for predictions to make
db_name = "small"
table_name = "Ratings"
test_csv_name = "comp3208-test-small"
#test_csv_name = "test_prediction"


# Create item data dictionary
start_time = time()

local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir, "..", "..", "Data", "Databases", db_name + ".db")
connection = sqlite3.connect(db_path)
cur = connection.cursor()
print("> Connected to database")

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

user_avgs = {}
for row in cur.execute(f"SELECT UserID, AVG(rating)  FROM {table_name} GROUP BY UserID"):
    user_avgs[row[0]] = row[1]
print("> Build User Averages dictionary")

# Load similarity matrix
sim_matrix_path = os.path.join(local_dir, "..", "..", "Data", "Output", "sim-matrix-" + db_name + ".npy")
sim_matrix = np.load(sim_matrix_path)
print("> Loaded similarity matrix of size:", sim_matrix.shape)
#

# Get list of (user, item, time) predictions to make
test_csv_path = os.path.join(local_dir, "..", "..", "Data", "CSV", test_csv_name + ".csv")
with open(test_csv_path) as csv_file:
    lines = csv.DictReader(csv_file, fieldnames=['userID', 'itemID', 'time'])
    data_entries = [(i['userID'], i['itemID'], i['time']) for i in lines]
print("> Read CSV file")

# dict item: -> (user: -> time)
input_dict = {}
for line in data_entries:
    user = int(line[0])
    item = int(line[1])
    time = int(line[2])
    if item in input_dict:
        input_dict[item][user] = time
    else:
        input_dict[item] = {user: time}

# Generate predictions
predictions = {}

for item, data in tqdm(input_dict.items()):
    predictions[item] = prd.get_prediction(item, data, items, all_item_data, sim_matrix, user_avgs)

output = []
for item, data in predictions.items():
    for user, rating in data.items():
        output.append((user, item, rating))


# Write predictions csv file
date = datetime.now().strftime("%d%m%Y-%H%M%S")
predictions_path = os.path.join(local_dir, "..", "..", "Data", "Output", "predictions-" + db_name + date + ".csv")

with open(predictions_path,'w', newline='') as results:
    csv_results = csv.writer(results)
    for entry in output:
        csv_results.writerow(entry)
