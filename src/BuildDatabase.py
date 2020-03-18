# File for building SQLite database
# http://www.grroups.com/blog/sqlite-working-with-large-data-sets-in-python-effectively

# Create and set-up database
import sqlite3
import csv
import time
import os

database_name = "small"
table_name = "ratings"
csv_name = "example-train"
# csv_name = "comp3208-train-small"

local_dir = os.path.dirname(__file__)
csv_path = os.path.join(local_dir, "../Data/" + csv_name + ".csv")

start_time = time.clock()
connection = sqlite3.connect(database_name + ".db")
cur = connection.cursor()

# Create the table
cur.execute(f"CREATE TABLE {table_name} (userID INTEGER, itemID INTEGER, rating FLOAT, time INTEGER, PRIMARY KEY (userID, itemID));")


with open(csv_path) as input:
    lines = csv.DictReader(input, fieldnames=['userID', 'itemID', 'rating', 'time'])
    data_entries = [(i['userID'], i['itemID'], i['rating'], i['time']) for i in lines]

cur.executemany(f"INSERT INTO {table_name} (userID, itemID, rating, time) VALUES (?, ?, ?, ?);", data_entries)
connection.commit()
connection.close()

elapsed_time = time.clock() - start_time
print("Time elapsed: {} seconds".format(elapsed_time))
