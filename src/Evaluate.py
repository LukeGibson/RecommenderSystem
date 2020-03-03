# Method for evaluating the predictions made
# Input dictionary mapping tuple(userID, itemID) to rating for both prediction and ground truth
# Uses named tuples: https://stackoverflow.com/questions/4878881/python-tuples-dictionaries-as-keys-select-sort
# Named tuples in dictionary's make things much easier
from collections import namedtuple
from math import pow
import csv
import os
# Example of making a value in dict
UserProductID = namedtuple("UserProductID", ["UserID", "ProductID"])

predictions_dict = {}
predictions_dict2 = {}

predictions_dict[UserProductID(UserID=1, ProductID=20)] = 4.2
predictions_dict2[UserProductID(UserID=1, ProductID=20)] = 4.4
predictions_dict[UserProductID(UserID=2, ProductID=20)] = 3.2
predictions_dict2[UserProductID(UserID=2, ProductID=20)] = 4.0
predictions_dict[UserProductID(UserID=3, ProductID=20)] = 1.2
predictions_dict2[UserProductID(UserID=3, ProductID=20)] = 4.0


def calculate_MSE(pred_dict, val_dict):
    n = len(pred_dict)
    total = 0
    for x, y in pred_dict.items():
        total += pow(y - val_dict[x], 2)
    MSE = total / n
    return MSE


def create_val_dict(val_csv_path):
    file = open(val_csv_path, "r")
    reader = csv.reader(file, delimiter=',')
    val_dict = {}
    for row in reader:
        val_dict[UserProductID(UserID=row[0], ProductID=row[1])] = row[2]
    return val_dict


local_dir = os.path.dirname(__file__)
size = "small"
no = 0
val_path = os.path.join(local_dir, "../Data/" + size + "Validation" + str(no) + ".csv")
valid_dict = create_val_dict(val_path)
for x, y in valid_dict.items():
    print(x, y)
print(f"MSE = {calculate_MSE(predictions_dict, predictions_dict2)}")
