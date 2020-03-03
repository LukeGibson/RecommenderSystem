# File for creating n random train validation CSV files,
# these can then be made into databases later on
import pandas as pd

inputPath = "../Data/example-train.csv"
size = "small"
df = pd.read_csv(inputPath, names=['userId', 'itemId', 'rating', 'time'])

for i in range(5):
    from sklearn.model_selection import train_test_split
    train, test = train_test_split(df, test_size=0.2)

    trainPath = "../Data/" + size + "Train" + str(i) + ".csv"
    valPath = "../Data/" + size + "Validation" + str(i) + ".csv"
    train.to_csv(trainPath, index=False, header=False)
    test.to_csv(valPath, index=False, header=False)
