import sqlite3
import csv
from time import process_time as time
import os


local_dir = os.path.dirname(__file__)
db_name = "ItemBased"
table_name = "Ratings"
db_path = os.path.join(local_dir, "..", "..", "Data", "Databases", db_name + ".db")
connection = sqlite3.connect(db_path)
cur = connection.cursor()

# for row in cur.execute(f"SELECT COUNT(DISTINCT ItemID) FROM {table_name}"):
#     print(row)

# items = []
# for row in cur.execute(f"SELECT DISTINCT(ItemID) FROM {table_name}"):
#     items.append(row[0])
# print(items)

# item_avgs = {}
# for row in cur.execute(f"SELECT ItemID, AVG(rating)  FROM {table_name} GROUP BY ItemID"):
#     item_avgs[row[0]] = row[1]
#
# print(item_avgs[1])

# for row in cur.execute(f"SELECT UserID, Rating FROM {table_name} WHERE ItemID = 3"):
#     print(row)
# (98801, 3.0)
# (111832, 2.5)
# (116061, 3.5)
# (148502, 3.5)
# (156442, 4.5)
# (206085, 3.0)
# (229595, 3.0)

count = []
for row in cur.execute(f"SELECT ItemID, COUNT(UserID) FROM {table_name} GROUP BY ItemID"):
    count.append((row[0], row[1]))
count.sort(key=lambda tup: tup[1], reverse=True)
total = 0
for c in count:
    if c[1] > 10000:
        total += 1
    print(c)
print(total)