import sqlite3
import os
from src import MakePrediction

local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir, 'ratings.db')
connection = sqlite3.connect(db_path)
cur = connection.cursor()


# Tests
u, i, r = MakePrediction.get_prediction(1, 8547, cur)
print("user", u, "for item", i, "has predicted rating", r) 

