# File for building SQLite database
# http://www.grroups.com/blog/sqlite-working-with-large-data-sets-in-python-effectively

# Create and set-up database
import sqlite3, csv
import time
import os

databasePath = 'Data/comp3208-train-small.csv'
databaseFileName = 'ratings.db'
databaseTableName = 'ratings'

start_time = time.clock()

local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir, '../ratings.db')
connection = sqlite3.connect(db_path)
cur = connection.cursor()
# Create the table
cur.execute("CREATE TABLE ratings (userID INT, itemID INT, rating FLOAT, time INT);")

with open(databasePath) as input:
    lines = csv.DictReader(input, fieldnames=['userID', 'itemID', 'rating', 'time'])
    data_entries = [(i['userID'], i['itemID'], i['rating'], i['time']) for i in lines]

cur.executemany("INSERT INTO ratings (userID, itemID, rating, time) VALUES (?, ?, ?, ?);", data_entries)
connection.commit()
connection.close()

elapsed_time = time.clock() - start_time
print("Time elapsed: {} seconds".format(elapsed_time))
