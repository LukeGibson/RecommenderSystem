import sqlite3
import os
from src import MakePrediction

name = "ratings"
local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir,  name + '.db')
connection = sqlite3.connect(db_path)
cur = connection.cursor()


# Tests
u = 1
i = 3
r = MakePrediction.get_prediction(u, i, name, cur)
print("user", u, "for item", i, "has predicted rating", r)

