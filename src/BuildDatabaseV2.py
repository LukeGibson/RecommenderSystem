import sqlite3
import csv
import time
import os
import gc
import math

database_name = "ratingsV2"
large_table_name = "ratings_main"
# csv_name = "example-train"
csv_name = "comp3208-train-small"

local_dir = os.path.dirname(__file__)
csv_path = os.path.join(local_dir, "../Data/" + csv_name + ".csv")

start_time = time.clock()
connection = sqlite3.connect(database_name + ".db")
cur = connection.cursor()

with open(csv_path) as input:
    lines = csv.DictReader(input, fieldnames=['userID', 'itemID', 'rating', 'time'])
    data_entries = [(i['userID'], i['itemID'], i['rating'], i['time']) for i in lines]

# Create the table
cur.execute(f"CREATE TABLE {large_table_name} (userID INTEGER, itemID INTEGER, rating FLOAT, time INTEGER, PRIMARY KEY (userID, itemID));")
cur.executemany(f"INSERT INTO {large_table_name} (userID, itemID, rating, time) VALUES (?, ?, ?, ?);", data_entries)

# used a check that data entries is finished
data_entries.append((-1, 0, 0, 0))


def round_to_5000(x):
    return int(math.ceil(int(x) / 5_000)) * 5000


current_range = 0
current_table = None
current_entries = []
count = 0
for i in data_entries:
    i_user = i[0]
    if round_to_5000(i_user) == current_range:
        current_entries.append((i[0], i[1], i[2], i[3]))
        count += 1
    else:
        if i_user == -1:
            print("Making_", current_table)
            cur.execute(
                f"CREATE TABLE {current_table} (userID INTEGER, itemID INTEGER, rating FLOAT, time INTEGER, PRIMARY KEY (userID, itemID));")

            cur.executemany(f"INSERT INTO {current_table} (userID, itemID, rating, time) VALUES (?, ?, ?, ?);",
                            current_entries)
            connection.commit()
            connection.close()
            break

        if current_table is not None:

            print("Making", current_table)
            cur.execute(
                f"CREATE TABLE {current_table} (userID INTEGER, itemID INTEGER, rating FLOAT, time INTEGER, PRIMARY KEY (userID, itemID));")

            cur.executemany(f"INSERT INTO {current_table} (userID, itemID, rating, time) VALUES (?, ?, ?, ?);",
                            current_entries)
            connection.commit()

        current_range = round_to_5000(i_user)
        current_table = "users_to_" + str(current_range) + "_ratings"
        current_entries = [(i[0], i[1], i[2], i[3])]
        gc.collect()
        count += 1


elapsed_time = time.clock() - start_time
print("Time elapsed: {} seconds".format(elapsed_time))