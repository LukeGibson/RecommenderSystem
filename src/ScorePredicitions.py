import sqlite3
import os
from time import time
from src import MakePredictionPandas
import pandas as pd

name = "validation"
local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir,  name + '.db')
connection = sqlite3.connect(db_path)
cur = connection.cursor()

valid_csv_path = "../Data/smallValidation0.csv"
valid_df = pd.read_csv(valid_csv_path, names=['userID', 'itemID', 'rating', 'time'],
                       dtype={'userID': int, 'itemID': int, 'rating': str, 'time': int}).set_index(['userID', 'itemID'])
valid_df['pred'] = -1
print(valid_df.head)

start = time()

current_user = 0
item_list = []
for index, row in valid_df.iterrows():
    if index[0] == current_user:
        item_list.append(index[1])
    else:
        if not current_user == 0:
            # new user so make the predictions for the last group and put the predictions into the db
            predictions = MakePredictionPandas.get_prediction(current_user, item_list, "ratings", cur)
            for i in range(len(predictions)):
                valid_df.loc[(current_user, item_list[i])]['pred'] = predictions[i]

        # now set up for the new user
        current_user = index[0]
        item_list.clear()
        item_list.append(index[1])

end = time()
