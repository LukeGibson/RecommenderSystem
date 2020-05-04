import os
import csv
import numpy as np
from matplotlib import pyplot as plt


graph_title = "Ratings per Item"

local_dir = os.path.dirname(__file__)
input_path = os.path.join(local_dir, "..", "..", "Data", "Output", "counts-small.csv")
output_path = os.path.join(local_dir, "..", "..", "Data", "Output", "Graphs", graph_title + '.png')


# open input file 
with open(input_path) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    entries = []
    for row in csv_reader:
        entries.append(row)

# get values from input
counts = []
for entry in entries:
    counts.append(int(entry[1]))

# get average value
avg = np.mean(counts)
print("Average Count:", avg)

# plot values
xPoints = np.array([x for x in range(0, len(counts))])
yPoints = np.array(counts)

fig = plt.figure(figsize=(16,9))
plt.plot(xPoints, yPoints)

# set labels
plt.xlabel('Item')
plt.ylabel('No. of Ratings')
plt.title(graph_title)

plt.grid(b=True, which='both', linestyle='--') 
plt.show()

# save graph as png
fig.savefig(output_path)

