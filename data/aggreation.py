folders = ['centralized', 'decentralized', 'federated']
# folders = ['centralized', 'centralized', 'federated']
import os
from collections import defaultdict
import matplotlib.pyplot as plt
res = defaultdict(dict)
fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(12, 4))
no_transaction = 1000
sendRates = [5, 10, 20, 50]
operations = ["login"]
plots = [ax1,ax2,ax3,ax4]
for operation in operations:
    for p, sendRate in enumerate(sendRates):
        for folder in folders:
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
        for folder in folders:
            pathName = f"./{no_transaction}_{sendRate}/" + folder + f"/{operation}/"
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

        # for i in res:
        #     for j in res[i]:
        #         res[i][j] = res[i][j] / no_transaction
        # print(res)
        # import matplotlib.pyplot as pp
        # pp.plot([i / no_transaction for i in raw_data["centralized"]['postgres']],  color='blue', label='postgres')
        # pp.plot([i / no_transaction for i in raw_data["centralized"]['python']],  color='red', label='python')

        from itertools import zip_longest
            
        sumPower = defaultdict(list)
        for folder in folders:
            sums = []
            for values in zip_longest(*raw_data[folder].values(), fillvalue=0):
                sums.append(sum(values)/10)
            sumPower[folder] = sums
            

        print(sumPower)  # Output: [14, 17, 10, 4]

        
        import numpy as np

        plots[p].plot(sumPower['centralized'], 'r', label='Centralized')
        plots[p].plot(sumPower['federated'], 'b', label='Federated')
        plots[p].plot(sumPower['decentralized'], 'g', label='Decentralized')
        plots[p].set_title(f'{sendRate}/Second')
        plots[p].set_ylabel('Watts')
        plots[p].set_xlabel('Seconds')
        plots[p].legend()
        means = [sum(sumPower['centralized'])/no_transaction, sum(sumPower['decentralized'])/no_transaction, sum(sumPower['federated'])/no_transaction]
        plt.figure()
        colors = ['red', 'blue', 'green']
        plt.bar(folders, means, color=colors)
        print(means)        
        plt.ylabel('Watt')
        plt.title(f'Average Power Consumption for {operation} per request at {sendRate}/second')
        # # add a legend
        plt.legend()
        plt.savefig(f'barchart_{sendRate}_for_{operation}')
        # means = [str(round(i, 2)) for i in means]
        # plots[p].text(0.5, 0.9, f'mean: {",".join(means)}', transform=plots[p].transAxes, fontsize=10, va='top', ha='center')

# fig.suptitle(f'Power consumption of Identity solutions for {operations[0]} operation')
# plt.tight_layout()
# Show the plot
# plt.show()
# plt.savefig(f'all_for_{operations[0]}.png')



        # create a new figure single 
        # plt.figure()

        # # plot each dataset in a different color
        # plt.plot(sumPower['centralized'], 'r', label='Centralized')
        # plt.plot(sumPower['federated'], 'b', label='Federated')
        # plt.plot(sumPower['decentralized'], 'g', label='Decentralized')

        # # set the axis labels and title
        # plt.xlabel('Seconds')
        # plt.ylabel('Watt')
        # plt.title(f'Power consumption of Identity solutions for {sendRate} {operation.capitalize()}/Second')

        # # add a legend
        # plt.legend()
        # plt.savefig(f'{sendRate}_for_{operation}.png')
        # show the plot
        # plt.show()


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
