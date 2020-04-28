# File for building SQLite database
# http://www.grroups.com/blog/sqlite-working-with-large-data-sets-in-python-effectively

# Create and set-up database
import sqlite3
import csv
from time import process_time as time
import os


csv_name = "comp3208-train-small"
local_dir = os.path.dirname(__file__)
csv_path = os.path.join(local_dir, "..", "..", "Data", "CSV", csv_name + ".csv")

start_time = time()
db_name = "ItemBased"
table_name = "Ratings"
db_path = os.path.join(local_dir, "..", "..", "Data", "Databases", db_name + ".db")
connection = sqlite3.connect(db_path)
cur = connection.cursor()


# Create the table
cur.execute(f"CREATE TABLE {table_name} (itemID INTEGER, userID INTEGER, rating FLOAT, time INTEGER, PRIMARY KEY (itemID, userID));")
print(f"> Database table \"{table_name}\" made")


with open(csv_path) as csv_file:
    lines = csv.DictReader(csv_file, fieldnames=['userID', 'itemID', 'rating', 'time'])
    entries = [(i['itemID'], i['userID'], i['rating'], i['time']) for i in lines]
print("> CSV read")

entries.sort(key=lambda tup: tup[0])
print("> Entries sorted")

cur.executemany(f"INSERT INTO {table_name} (itemID, userID, rating, time) VALUES (?, ?, ?, ?);", entries)
connection.commit()
connection.close()
print(f"> Entries added to {table_name}")

elapsed_time = time() - start_time
print(f"Time elapsed: {elapsed_time} seconds")
