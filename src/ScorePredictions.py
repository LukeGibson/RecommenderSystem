import sqlite3
import os
import csv
from time import time
from math import pow, ceil, floor
from tqdm import tqdm
import MakePredictionV2
import random

name = "validation"
# name = "UserItemTables"
local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir,  name + '.db')
connection = sqlite3.connect(db_path)
cur = connection.cursor()

csv_path = "Data/smallValidation.csv"


with open(csv_path) as csv_file:
    lines = csv.DictReader(csv_file, fieldnames=['userID', 'itemID', 'rating', 'time'])
    data_entries = [(i['userID'], i['itemID'], i['rating'], i['time']) for i in lines]

start = time()
for i in range(3):
    sample_list = random.sample(data_entries, sample_size)
    round_total, floor_total, ceil_total = 0, 0, 0
    n = len(sample_list)

        user = int(line[0])
        item_list = [int(line[1])]
        rating = float(line[2])

        predictions = MakePrediction.get_prediction(user, item_list, "ratings", cur)
        # predictions = MakePredictionV2.get_prediction(user, item_list, "User_table", "Item_table", cur)

        if predictions is not None:
            pred = predictions[0]
            round_05 = round(pred * 2) / 2
            ceil_05 = ceil(pred * 2) / 2
            floor_05 = floor(pred * 2) / 2
            # print(user, item_list)
            # print(f"True Value: {pred}, Rounded pred: {round_05}, Ceil pred: {ceil_05}, Floor pred: {floor_05}")
            round_total += pow(round_05 - rating, 2)
            floor_total += pow(floor_05 - rating, 2)
            ceil_total += pow(ceil_05 - rating, 2)
        else:
            n -= 1

    print(f"MSE for rounding = {round_total / n}")
    print(f"MSE for flooring = {floor_total / n}")
    print(f"MSE for ceiling = {ceil_total / n}")

print(f"Total time taken: {time() - start}")

