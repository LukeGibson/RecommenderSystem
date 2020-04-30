import os
import csv


# Name cvs file for predictions to make
db_name = "small"
local_dir = os.path.dirname(__file__)


# Get list of (user, item, time) predictions to make
test_csv_path = os.path.join(local_dir, "..", "..", "Data", "Output", "predictions-" + db_name + ".csv")

with open(test_csv_path) as csv_file:
    lines = csv.DictReader(csv_file, fieldnames=['userID', 'itemID','rating', 'time'])
    ratings_to_predict = [(i['userID'], i['itemID'], i['rating'], i['time']) for i in lines]


# Generate predictions
predictions = []

for entry in ratings_to_predict:
    user = int(entry[0])
    item = int(entry[1])
    rating = float(entry[2])

    predictions.append((user, item, rating))


# Write predictions csv file
predictions_path = os.path.join(local_dir, "..", "..", "Data", "Output", "predictions-notime-" + db_name + ".csv")

with open(predictions_path,'w', newline='') as results:
    csv_results = csv.writer(results)
    for entry in predictions:
        csv_results.writerow(entry)