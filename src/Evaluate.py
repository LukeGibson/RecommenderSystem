# Method for evaluating the predictions made
# Input dictionary mapping tuple(userID, itemID) to rating for both prediction and ground truth
# Uses named tuples: https://stackoverflow.com/questions/4878881/python-tuples-dictionaries-as-keys-select-sort
# Named tuples in dictionary's make things much easier
from collections import namedtuple
# Example of making a value in dict
UserProductID = namedtuple("UserProductID", ["UserID", "ProductID"])
predictions_dict = {UserProductID(UserID=1, ProductID=20) : 4.2}
a = UserProductID(UserID=1, ProductID=22)

def evaluate(predictions_dict, validation_dict):
