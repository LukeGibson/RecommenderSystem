# File for creating n random train validation CSV files,
# these can then be made into databases later on
import pandas as pd
import os
from collections import OrderedDict
from tqdm import tqdm
import numpy as np
local_dir = os.path.dirname(__file__)
size = "small"
csv_path = os.path.join(local_dir, '../Data/comp3208-train-' + size + '.csv')
df = pd.read_csv(csv_path, names=['userID', 'itemID', 'rating', 'time'],
                 dtype={'userID': int, 'itemID': int, 'rating': str, 'time': int}).set_index(['userID', 'itemID'])

# go through the users and take on out and add that to the validation df and add all the other items to the train df
# dtypes = np.dtype([
#           ('userID', int),
#           ('itemID', int),
#           ('rating', float),
#           ('time', int),
#           ])
# data = numpy.empty(0, dtype=dtypes)
# df = pandas.DataFrame(data)
train_df = pd.DataFrame(columns=['userID', 'itemID', 'rating', 'time']).set_index(['userID', 'itemID'])
test_df = pd.DataFrame(columns=['userID', 'itemID', 'rating', 'time']).set_index(['userID', 'itemID'])

# needs reworking so that each user has one item in the validation set and the rest in the training
# otherwise some users could end up only in the valid csv and not in the training giving incomplete data for predictions

index_list = list(OrderedDict.fromkeys(df.index.get_level_values(0)))
# go through all of the users in 'df'
# print(df.loc[index_list[0]][-1:])
# print("-")
# print(df.loc[index_list[0]][:-1])

train_dict = {"userID": [], "itemID": [], "rating": [], "time": []}
test_dict = {"userID": [], "itemID": [], "rating": [], "time": []}
for i in tqdm(index_list, ):
    lines = df.loc[i][:-1]
    for j in range(len(lines['rating'])):
        train_dict["userID"].append(i)
        train_dict["itemID"].append(lines.index[j])
        train_dict["rating"].append(lines.values[j][0])
        train_dict["time"].append(lines.values[j][1])
    line = df.loc[i][-1:]
    test_dict["userID"].append(i)
    test_dict["itemID"].append(line.index[0])
    test_dict["rating"].append(line.values[0][0])
    test_dict["time"].append(line.values[0][1])
train_df = train_df.append(pd.DataFrame.from_dict(train_dict), sort=True).set_index(['userID', 'itemID'])
a = train_df.index.get_level_values(0).astype(int)
b = train_df.index.get_level_values(1).astype(int)
train_df.index = [a, b]
test_df = test_df.append(pd.DataFrame.from_dict(test_dict), sort=True).set_index(['userID', 'itemID'])
a = test_df.index.get_level_values(0).astype(int)
b = test_df.index.get_level_values(1).astype(int)
test_df.index = [a, b]



# output the df's to csv files
trainPath = os.path.join(local_dir, "../Data/" + size + "Train.csv")
valPath = os.path.join(local_dir, "../Data/" + size + "Validation.csv")
train_df.to_csv(trainPath, index=True, header=False)
test_df.to_csv(valPath, index=True, header=False)
