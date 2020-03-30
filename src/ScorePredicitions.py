import sqlite3
import os
import csv
from time import time
from math import pow
from tqdm import tqdm
from src import MakePredictionPandas

name = "validation"
local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir,  name + '.db')
connection = sqlite3.connect(db_path)
cur = connection.cursor()

csv_path = "../Data/smallValidation.csv"
start = time()

with open(csv_path) as csv_file:
    lines = csv.DictReader(csv_file, fieldnames=['userID', 'itemID', 'rating', 'time'])
    data_entries = [(i['userID'], i['itemID'], i['rating'], i['time']) for i in lines]


total = 0
n = len(data_entries)
# count = 0
for i in tqdm(data_entries):
    user = int(i[0])
    item_list = [int(i[1])]
    rating = float(i[2])
    # count += 1
    # if count < 10:
    #     print(i)
    #     print(f"UserID: {i[0]}, ItemID: {i[1]}, Rating: {i[2]}")
    predictions = MakePredictionPandas.get_prediction(user, item_list, "ratings", cur)
    print(predictions)
    total += pow(predictions[0] - rating, 2)
end = time()

MSE = total / n

print(f"MSE for validation set = {MSE}")
print(f"Total time taken: {end - start}")

