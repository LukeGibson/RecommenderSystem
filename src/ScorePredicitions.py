import sqlite3
import os
import csv
from time import time
from math import pow, ceil, floor
from tqdm import tqdm
import MakePredictionPandas
import random

name = "validation"
local_dir = os.path.dirname(__file__)
db_path = os.path.join(local_dir,  name + '.db')
connection = sqlite3.connect(db_path)
cur = connection.cursor()

csv_path = "Data/smallValidation.csv"
start = time()

with open(csv_path) as csv_file:
    lines = csv.DictReader(csv_file, fieldnames=['userID', 'itemID', 'rating', 'time'])
    data_entries = [(i['userID'], i['itemID'], i['rating'], i['time']) for i in lines]

for i in range(3):
    random.seed(50) # fixed seed to make sample_list constant
    sample_size = 1_000
    sample_list = random.sample(data_entries, sample_size)
    total = 0
    n = len(sample_list)
    # count = 0
    for line in tqdm(sample_list):
        user = int(line[0])
        item_list = [int(line[1])]
        rating = float(line[2])

        predictions = MakePredictionPandas.get_prediction(user, item_list, "ratings", cur)

        if predictions is not None:
            pred = predictions[0]
            round_05 = round(pred * 2) / 2
            ceil_05 = ceil(pred * 2) / 2
            floor_05 = floor(pred * 2) / 2
            print(f"True Value: {pred}, Rounded pred: {round_05}, Ceil pred: {ceil_05}, Floor pred: {floor_05}")
            total += pow(predictions[0] - rating, 2)
        else:
            n -= 1
    end = time()

    MSE = total / n

    print(f"MSE for validation set = {MSE}")
    print(f"Total time taken: {end - start}")

