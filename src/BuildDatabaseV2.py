# File for building SQLite database
# http://www.grroups.com/blog/sqlite-working-with-large-data-sets-in-python-effectively

# Create and set-up database
import sqlite3
import csv
import time
import os

database_name = "ExampleTables"
user_table_name = "User_table"
item_table_name = "Item_table"
csv_name = "example-train"
# csv_name = "comp3208-train-small"
# csv_name = "smallTrain"

local_dir = os.path.dirname(__file__)
csv_path = os.path.join(local_dir, "../Data/" + csv_name + ".csv")

start_time = time.clock()
connection = sqlite3.connect(database_name + ".db")
cur = connection.cursor()

# Create the table
cur.execute(f"CREATE TABLE {user_table_name} (userID INTEGER, itemID INTEGER, rating FLOAT, time INTEGER, PRIMARY KEY (userID, itemID));")
cur.execute(f"CREATE TABLE {item_table_name} (itemID INTEGER, userID INTEGER, PRIMARY KEY (itemID, userID));")


with open(csv_path) as input:
    lines = csv.DictReader(input, fieldnames=['userID', 'itemID', 'rating', 'time'])
    user_entries = [(i['userID'], i['itemID'], i['rating'], i['time']) for i in lines]
    item_entries = [(j[1], j[0]) for j in user_entries]

cur.executemany(f"INSERT INTO {user_table_name} (userID, itemID, rating, time) VALUES (?, ?, ?, ?);", user_entries)
connection.commit()
cur.executemany(f"INSERT INTO {item_table_name} (itemID, userID) VALUES (?, ?);", item_entries)
connection.commit()
connection.close()

elapsed_time = time.clock() - start_time
print("Time elapsed: {} seconds".format(elapsed_time))
