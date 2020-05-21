import sqlite3
import csv
from time import process_time as time
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict


local_dir = os.path.dirname(__file__)
db_name = "small"
table_name = "Ratings"
db_path = os.path.join(local_dir, "..", "..", "Data", "Databases", db_name + ".db")
connection = sqlite3.connect(db_path)
cur = connection.cursor()

# total = 0
# for row in cur.execute(f"SELECT * FROM {table_name}"):
#     total += 1
# print(total)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize =(25,10))
counts_u = []
for row in cur.execute(f"SELECT ItemID, COUNT(ItemID) FROM {table_name} GROUP BY ItemID"):
    counts_u.append(row[1])
# print(len([x for x in counts if x > 500]))
bins = np.arange(start=0, stop=501, step=25)
ax1.hist(counts_u, density=False, bins=bins)
ax1.set_title("Frequency of the number of ratings per item in dataset")
ax1.set(xlabel='Number of Ratings per Item', ylabel='Frequency')
# plt.show()

counts_i = []
for row in cur.execute(f"SELECT UserID, COUNT(UserID) FROM {table_name} GROUP BY UserID"):
    counts_i.append(row[1])
# print(len([x for x in counts if x > 500]))
# (range(len(counts)), list(counts.keys()))
bins_u = np.arange(start=0, stop=501, step=25)
ax2.hist(counts_i, density=False, bins=bins_u)
ax2.set_title("Frequency of the number of ratings per user in dataset")
ax2.set(xlabel='Number of Ratings per User', ylabel='Frequency')
#plt.show()
# 1008

# counts = {}
# for row in cur.execute(f"SELECT Rating FROM {table_name} "):
#     try:
#         rat = float(row[0])
#         counts[rat] = counts.get(rat, 0) + 1
#     except ValueError:
#         pass
# counts = OrderedDict(sorted(counts.items()))
# ax3.bar(range(len(counts)), list(counts.values()), align='center')
# ax3.set(xlabel='Rating',ylabel='Frequency')

plt.show()

# from statistics import mean
# zero_s = []
# two_point_five_s = []
# three_point_five_s = []
# five_s = []
# zero_a = []
# two_point_five_a = []
# three_point_five_a = []
# five_a = []
# raw = []
# for row in cur.execute(f"SELECT Rating FROM {table_name}"):
#     try:
#         rat = float(row[0])
#         z = abs(rat - 0)
#         h = abs(rat - 2.5)
#         t = abs(rat - 3.5)
#         f = abs(rat - 5)
#         zero_s.append(pow(z, 2))
#         two_point_five_s.append(pow(h, 2))
#         three_point_five_s.append(pow(t, 2))
#         five_s.append(pow(f, 2))
#         zero_a.append(z)
#         two_point_five_a.append(h)
#         three_point_five_a.append(t)
#         five_a.append(f)
#     except ValueError:
#         pass
# print(f"Zero MSE {mean(zero_s)}")
# print(f"Zero MAE {mean(zero_a)}")
# print(f"2.5 MSE {mean(two_point_five_s)}")
# print(f"2.5 MAE {mean(two_point_five_a)}")
# print(f"3.5 MSE {mean(three_point_five_s)}")
# print(f"3.5 MAE {mean(three_point_five_a)}")
# print(f"5 MSE {mean(five_s)}")
# print(f"5 MAE {mean(five_a)}")

# from statistics import mean
# user_avgs = {}
# for row in cur.execute(f"SELECT UserID, AVG(rating) FROM {table_name} GROUP BY UserID"):
#     user_avgs[row[0]] = row[1]
# MSE = []
# MAE = []
# for row in cur.execute(f"SELECT UserID, Rating FROM {table_name} "):
#     try:
#         dif = float(row[1]) - user_avgs[row[0]]
#         MSE.append(pow(dif, 2))
#         MAE.append(abs(dif))
#     except ValueError:
#         pass
# print(f"MSE: {mean(MSE)}")
# print(f"MAE: {mean(MAE)}")

# from statistics import mean
# item_avgs = {}
# for row in cur.execute(f"SELECT ItemID, AVG(rating) FROM {table_name} GROUP BY ItemID"):
#     item_avgs[row[0]] = row[1]
# MSE = []
# MAE = []
# for row in cur.execute(f"SELECT ItemID, Rating FROM {table_name}"):
#     try:
#         dif = float(row[1]) - item_avgs[row[0]]
#         MSE.append(pow(dif, 2))
#         MAE.append(abs(dif))
#     except ValueError:
#         pass
# print(f"MSE: {mean(MSE)}")
# print(f"MAE: {mean(MAE)}")


# items = []
# for row in cur.execute(f"SELECT DISTINCT(ItemID) FROM {table_name}"):
#     items.append(row[0])
# print(items)

# item_avgs = {}
# for row in cur.execute(f"SELECT ItemID, AVG(rating)  FROM {table_name} GROUP BY ItemID"):
#     item_avgs[row[0]] = row[1]
#
# print(item_avgs[1])

# user_avgs = {}
# for row in cur.execute(f"SELECT UserID, AVG(rating)  FROM {table_name} GROUP BY UserID"):
#     user_avgs[row[0]] = row[1]
# print(user_avgs[2])

# for row in cur.execute(f"SELECT UserID, Rating FROM {table_name} WHERE ItemID = 3"):
#     print(row)
# (98801, 3.0)
# (111832, 2.5)
# (116061, 3.5)
# (148502, 3.5)
# (156442, 4.5)
# (206085, 3.0)
# (229595, 3.0)

# for row in cur.execute(f"SELECT UserID, AVG(rating) FROM {table_name} GROUP BY UserID"):
#     user_avgs[row[0]] = row[1]
# print("> Calculated user averages")
# print(user_avgs[2])
# for row in cur.execute(f"SELECT UserID, rating FROM {table_name} WHERE UserID = 2"):
#     print(row)

