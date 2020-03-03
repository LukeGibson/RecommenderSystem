# File containing possible queries that can be ran on a pre-existing db
# import time
# start_time = time.clock()
import sqlite3
import os

local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir, '../ratings.db')
connection = sqlite3.connect(db_path)
cur = connection.cursor()

# for loop over all rows ordered by userID
# for row in cur.execute('SELECT * FROM ratings ORDER BY userID'):
#     print(row)

# print all lines where userID = 40714, and rating is less that 2.5
# criteria = (40714, 2.5,)
# for row in cur.execute('SELECT itemID FROM ratings WHERE userID = ? AND rating <= ?', criteria):
#     print(row[0])

# Count number of rows in database
# cur.execute('SELECT * FROM ratings')
# print(len(cur.fetchall()))
# >>> 9425746

# Count number of unique users
# for row in cur.execute('SELECT COUNT(DISTINCT userID) FROM ratings;'):
#     print(row[0])
# >>> 274246

# Count number of unique items
# for row in cur.execute('SELECT COUNT(DISTINCT itemID) FROM ratings;'):
#     print(row[0])
# # >>> 19807

# database call - given userId get a users average rating (rounded to 2dp)
# user_ID = 1
# criteria = (user_ID,)
# rating = 0
# index = 0
# for row in cur.execute('SELECT AVG(rating) FROM ratings WHERE userID = ?', criteria):
#     rating = round(row[0], 2)
# print(rating)

# database call - given a userId and the sharedItems return the list of ratings
# user_ID = 1
# sharedItems = [12793, 113, 1876]
# ratings = []
# for i in range(len(sharedItems)):
#     criteria = (user_ID, sharedItems[i],)
#     for row in cur.execute('SELECT rating FROM ratings WHERE userID = ? AND itemID = ?', criteria):
#         ratings.append(row[0])
# print(ratings)
# u1Ratings = [8, 2, 7]
# u2Ratings = [2, 7, 5]

# database call - given 2 userId's return the list of itemId's they've both rated
# iD_1 = (1,)
# iD_2 = (2,)
# ratings1 = []
# ratings2 = []
# for row in cur.execute('SELECT itemID FROM ratings WHERE userID = ?', iD_1):
#     ratings1.append(row[0])
# for row in cur.execute('SELECT itemID FROM ratings WHERE userID = ?', iD_2):
#     ratings2.append(row[0])
# sharedItems = [v for v in ratings1 if v in ratings2]
# print(sharedItems)


# database call - given userItems get a list of userId's who also have a rating for at least 1 of the items
# itemList = [12793, 113, 1876]
# userList = []
# for i in range(len(itemList)):
#     criteria = (itemList[i],)
#     for row in cur.execute('SELECT userID FROM ratings WHERE itemID = ?', criteria):
#         userList.append(row[0])
# userList = list(dict.fromkeys(userList))
# print(userList)

criteria = (333333333, 2)
db_call = cur.execute('SELECT rating FROM ratings WHERE userID = ? AND itemID = ?', criteria)
for row in db_call:
    u2_item = row[0]
    print(u2_item + "!")
if db_call:
    print("t")