folders = ['centralized', 'decentralized', 'federated']
# folders = ['centralized', 'centralized', 'federated']
import os
from collections import defaultdict
res = defaultdict(dict)
no_transaction = 1000
sendRates = [5, 10, 20, 50]
operations = ["register", "login"]
for operation in operations:
    for folder in folders:
        for p, sendRate in enumerate(sendRates):
            res[folder] = defaultdict(float)
            pathName = f"./{no_transaction}_{sendRate}/" + folder + f"/{operation}/"
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
        raw_data[folder] = defaultdict(dict)
        for m, sendRate in enumerate(sendRates):
            pathName = f"./{no_transaction}_{sendRate}/" + folder + f"/{operation}/"
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
                raw_data[folder][sendRate][processName] = sums
            # Print the sums

        from itertools import zip_longest
        import matplotlib.pyplot as plt
        import numpy as np
        #Create the figure and subplots
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(12, 4))

        # Plot the data on each subplot
        plots = [ax1, ax2, ax3, ax4]
        ax1.set_title('sendRate = 5')
        ax2.set_title('sendRate = 10')
        ax3.set_title('sendRate = 20')
        ax4.set_title('sendRate = 50')
        ax1.set_ylabel('Watts')
        ax2.set_ylabel('Watts')
        ax3.set_ylabel('Watts')
        # Set the overall title
        fig.suptitle(f'Power consumption of {operation} operation in {folder} solution')
        fig.subplots_adjust(hspace=0.5, wspace=0.5)
        y_min = 99999
        y_max = 0
            # for m, folder in enumerate(folders):
            #     for processes in raw_data[folder]:
            #         y_min = min([i/no_transaction for i in raw_data[folder][processes]])
            #         y_max = max([i/no_transaction for i in raw_data[folder][processes]])


            # for p in plots:
            #     p.set_ylim(y_min, y_max)
            
        print(raw_data)
        for m, sendRate in enumerate(sendRates):
            for processes in raw_data[folder][sendRate]:
                d = [i/10 for i in raw_data[folder][sendRate][processes]]
                plots[m].plot(d, label=processes)
            plots[m].legend()    



        # add a legend
        plt.legend()

        # show the plot
        plt.savefig(f"{folder}_{operation}_processes.png")




        # # Show the plot
        # plt.show()
