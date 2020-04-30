# -------------------------------
# Given a item indexed database and test csv
# Build the similarity matix for the database
# Calculate the predicted ratings in the test csv
# Write the preditions to a file
# -------------------------------

import os
import sqlite3
import csv
import pandas as pd

import Prediction as prd
import Similarity as sim

# Input variables
db_name = "ratings"              # what to build sim matrix from
test_csv_name = "test"           # what predictions to make


# Access (previously built) itemId indexed ratings database
# Database format: ItemID, [UserID], [Rating], [Time]
local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir,  db_name + '.db')
connection = sqlite3.connect(db_path)
cur = connection.cursor()


# create dataframe / dictionary from database to store this in memory
item_ratings_df = pd.DataFrame()


# Compute similarity matrix from dataframe
simMatrix = sim.get_sim_matrix(item_ratings_df)


# Get list of (user, item, time) predictions to make
test_csv = os.path.join(local_dir, "Data", "CSV", test_csv_name, "csv")

with open(test_csv) as csv_file:
    lines = csv.DictReader(csv_file, fieldnames=['userID', 'itemID', 'time'])
    ratings_to_predict = [(i['userID'], i['itemID'], i['time']) for i in lines]


# Generate prediction list
predicted_ratings = []

for entry in ratings_to_predict:
    user = int(entry[0])
    item = int(entry[1])
    time = int(entry[2])

    prediction = prd.get_prediction(user, item, time)
    predicted_ratings.append(prediction)


# Write predictions csv file
