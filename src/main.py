import sqlite3
import os
import MakePredictionV2

name = "ExampleTables"
local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir,  name + '.db')
connection = sqlite3.connect(db_path)
cur = connection.cursor()


# Tests
u = 1
i = [3]
# r = MakePrediction.get_prediction(u, i, "User_table", cur)
r = MakePredictionV2.get_prediction(u, i, "User_table", "Item_table", cur)
print("user", u, "for item", i, "has predicted rating", r)

