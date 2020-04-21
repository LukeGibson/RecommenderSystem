import os
import numpy as np
from matplotlib import pyplot as plt


local_dir = str(os.path.dirname(__file__)) + "\\PredErrors\\"
fileNames = ["roundErrors.txt", "ceilErrors.txt", "floorErrors.txt"]

for fileName in fileNames:
        
    file_path = str(local_dir + fileName)
    error_file = open(file_path, 'r')

    abs_errors = []
    for pred in error_file.readlines():
        abs_errors.append(float(pred))


    # plot sorted absolute errors
    sorted_abs_errors = sorted(abs_errors)
    MAE = np.mean(abs_errors)
    print(fileName + " MAE:", MAE)

    xPoints = np.array([x for x in range(0, len(abs_errors))])
    yPoints = np.array(sorted_abs_errors)

    fig = plt.figure(figsize=(16,9))
    plt.plot(xPoints, yPoints)

    plt.xlabel('Entry Number')
    plt.ylabel('Absolute Error')
    plt.title(fileName)

    plt.grid(b=True, which='both', linestyle='--') 
    plt.show()


    # plot sorted squared errors
    sorted_square_errors = [x ** 2 for x in sorted_abs_errors]
    MSE = np.mean(sorted_square_errors)
    print(fileName + " MSE:", MSE)

    xPoints = np.array([x for x in range(0, len(abs_errors))])
    yPoints = np.array(sorted_square_errors)

    fig = plt.figure(figsize=(16,9))
    plt.plot(xPoints, yPoints)

    plt.xlabel('Entry Number')
    plt.ylabel('Squared Error')
    plt.title(fileName)

    plt.grid(b=True, which='both', linestyle='--') 
    plt.show()