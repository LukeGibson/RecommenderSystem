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
criteria = (40714, 2.5,)
for row in cur.execute('SELECT itemID FROM ratings WHERE userID = ? AND rating <= ?', criteria):
    print(row[0])