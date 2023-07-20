folders = ['centralized', 'decentralized_identity', 'federated']
# folders = ['centralized', 'centralized', 'federated']
import os
from collections import defaultdict
res = defaultdict(dict)
no_transaction = 1000
operation = "register"
for folder in folders:
    res[folder] = defaultdict(float)
    pathName = "./" + folder + f"/{operation}/"
    for i in range(1, 11):
        for file in os.listdir(pathName + str(i)):
            # check only text files
            if file.endswith('.csv'):
                processName = file.split('-')[0]
                with open(pathName + str(i) + "/" + file) as f:
                    lines = f.readlines()
                    cpuPower = 2
                    for line in lines[1:]:
                        if float(line.split(',')[cpuPower]) > 0:
                            res[folder][processName] += float(line.split(',')[cpuPower].strip())

# Initialize a list to store the sums
import csv
# Open each CSV file and sum the values at the same position
raw_data = {}
for folder in folders:
    pathName = "./" + folder + f"/{operation}/"
    raw_data[folder] = defaultdict(float)
    processNames = set()
    for file in os.listdir(pathName + "/1" ):
            if not file.endswith('.csv'):
                continue
            processNames.add(file.split('-')[0])
    for processName in processNames:
        sums = []
        for k in range(1, 11):
            for file in os.listdir(pathName + str(k)):
                if not file.endswith('.csv') or not file.startswith(processName):
                    continue
                with open(pathName + str(k) + "/" + file) as f:
                    reader = csv.reader(f)
                    for i, row in enumerate(reader):
                        if i == 0:
                            # Skip the header row
                            continue
                        if len(sums) < i:
                            # Add a new element to the sums list for each new column
                            sums.extend([0] * (i - len(sums)))
                        if float(row[2]) > 0:
                            sums[i-1] += float(row[2])
        raw_data[folder][processName] = sums
    # Print the sums

for i in res:
    for j in res[i]:
        res[i][j] = res[i][j] / no_transaction
# print(res)
# import matplotlib.pyplot as pp
# pp.plot([i / no_transaction for i in raw_data["centralized"]['postgres']],  color='blue', label='postgres')
# pp.plot([i / no_transaction for i in raw_data["centralized"]['python']],  color='red', label='python')

from itertools import zip_longest
    
sumPower = defaultdict(list)
for folder in folders:
    sums = []
    for values in zip_longest(*raw_data[folder].values(), fillvalue=0):
        sums.append(sum(values)/no_transaction/10)
    sumPower[folder] = sums
    

print(sumPower)  # Output: [14, 17, 10, 4]

import matplotlib.pyplot as plt
import numpy as np


# create a new figure
plt.figure()

# plot each dataset in a different color
plt.plot(sumPower['centralized'], 'r', label='Centralized')
plt.plot(sumPower['federated'], 'b', label='Federated')
plt.plot(sumPower['decentralized_identity'], 'g', label='decentralized')

# set the axis labels and title
plt.xlabel('Minutes')
plt.ylabel('Watt per transaction')
plt.title('Power consumption of different Identity solutions: ' + operation.capitalize())

# add a legend
plt.legend()

# show the plot
plt.show()


# Create the figure and subplots
# fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))

# # Plot the data on each subplot
# ax1.plot(sumPower['centralized'], color='blue', label='centralized')
# ax1.set_title('centralized Identity solution')
# ax2.plot(sumPower['decentralized_identity'], color='red', label='decentralized_identity')
# ax2.set_title('decentralized Identity solution')
# ax3.plot(sumPower['federated'], color='green', label='federated')
# ax3.set_title('federated Identity solution')
# ax1.set_ylabel('Watts per transaction')
# ax2.set_ylabel('Watts per transaction')
# ax3.set_ylabel('Watts per transaction')
# # Set the overall title
# fig.suptitle('Power consumption of different Identity solutions')
# fig.subplots_adjust(hspace=0.5, wspace=0.5)
# # Show the plot
# plt.show()
