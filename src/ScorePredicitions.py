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

print(lines)

# total = 0
# n = len(lines)
# for i in tqdm(lines):
#     pred = MakePredictionPandas.get_prediction(i['userID'], [i['itemID']], "ratings", cur)
#     total += pow(pred - i['rating'], 2)
# end = time()
#
# MSE = total / n
#
# print(f"MSE for validation set = {MSE}")
# print(f"Total time taken: {end - start}")

