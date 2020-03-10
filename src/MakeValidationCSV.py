# File for creating n random train validation CSV files,
# these can then be made into databases later on
import pandas as pd
import os
local_dir = os.path.dirname(__file__)
size = "small"
csv_path = os.path.join(local_dir, '../Data/comp3208-train-' + size + '.csv')
df = pd.read_csv(csv_path, names=['userId', 'itemId', 'rating', 'time'])
no_validation_sets = 1

for i in range(no_validation_sets):
    from sklearn.model_selection import train_test_split
    train, test = train_test_split(df, test_size=0.2)

    trainPath = os.path.join(local_dir, "../Data/" + size + "Train" + str(i) + ".csv")
    valPath = os.path.join(local_dir, "../Data/" + size + "Validation" + str(i) + ".csv")
    train.to_csv(trainPath, index=False, header=False)
    test.to_csv(valPath, index=False, header=False)
