# File containing possible queries that can be ran on a pre-existing db
import sqlite3
# import time
# start_time = time.clock()
connection = sqlite3.connect('ratings.db')
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
for row in cur.execute('SELECT COUNT(DISTINCT itemID) FROM ratings;'):
    print(row[0])
# >>> 19807
