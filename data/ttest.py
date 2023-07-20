import scipy.stats as stats

folders = ['centralized', 'decentralized', 'federated']
import os
from collections import defaultdict

res = defaultdict(dict)
no_transaction = 1000
sendRates = [5, 10, 20, 50]
operations = ["login"]

data_sendRate = defaultdict(dict)

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
            for values in list(zip_longest(*raw_data[folder].values(), fillvalue=0))[5:-5]:
                sums.append(sum(values)/10)
            sumPower[folder] = sums
        
        
        # calculate component difference
        for folder in folders:
            proc_data = [i for i in raw_data[folder].values()]
            k = len(proc_data)  # Number of groups
            N = sum([len(i) for i in proc_data])  # Total number of observations
            df_between = k - 1
            df_within = N - k
            f_statistic, p_value = stats.f_oneway(*proc_data)
            f_critical = stats.f.ppf(1 - 0.05, df_between, df_within)
            #Print the results
            if folder == "federated":
                print(f"comparison of processes in {folder} solution for {operation} at {sendRate} sendrate")
                # print(f"label order is : {list(raw_data[folder].keys())}")
                posthoc = stats.tukey_hsd(*raw_data[folder].values())
                # posthoc = stats.tukey_hsd(raw_data[folder]["postgres"], raw_data[folder]["findy"])
                print(posthoc)


                # print(f"F-Statistic for {folder} {sendRate} {operation}:", round(f_statistic,2))
                # print(f"for {folder} {operation} P-value:", p_value)
                # print("Degrees of freedom (between):", df_between)
                # print("Degrees of freedom (within):", df_within)
                # print("F critical value:", round(f_critical,4))
                
            

        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(1, 1)

        ax.boxplot([sumPower['centralized'], sumPower['decentralized'], sumPower['federated']])

        ax.set_xticklabels(["centralized", "decentralized", "federated"]) 

        ax.set_ylabel("mean") 

        # plt.show()

        # print(sumPower)  # Output: [14, 17, 10, 4]
        # Perform one-way ANOVA

        # Calculate degrees of freedom
        k = 3  # Number of groups
        N = len(sumPower['centralized']) + len(sumPower['decentralized']) + len(sumPower['federated'])  # Total number of observations
        
        df_between = k - 1
        df_within = N - k
        f_statistic, p_value = stats.f_oneway(sumPower['centralized'], sumPower['decentralized'], sumPower['federated'])
        if not operation in data_sendRate[sendRate]:
            data_sendRate[sendRate][operation] = defaultdict(dict)
        data_sendRate[sendRate][operation]["centralized"] = sumPower['centralized']
        data_sendRate[sendRate][operation]["decentralized"] = sumPower['decentralized']
        data_sendRate[sendRate][operation]["federated"] = sumPower['federated'] 
        # Print the results
        # print(f"F-Statistic for {sendRate} {operation}:", round(f_statistic,2))
        # print(f"for {sendRate} {operation} P-value:", p_value)
        # print("Degrees of freedom (between):", df_between)
        # print("Degrees of freedom (within):", df_within)
        
        f_critical = stats.f.ppf(1 - 0.05, df_between, df_within)

        # print("F critical value:", round(f_critical,4))
        # print(f"sendRate: {sendRate} Operations: {operation} ")
            # Perform Tukey's post-hoc test
        posthoc = stats.tukey_hsd(sumPower['centralized'],sumPower['decentralized'],sumPower['federated'])


        # print(posthoc)

#calculate impact of different sendrate
# for operation in operations:
#     for folder in folders:
#         k = 4  # Number of groups
#         N = len(data_sendRate[5][operation][folder]) + len(data_sendRate[10][operation][folder]) + len(data_sendRate[20][operation][folder]) + len(data_sendRate[50][operation][folder])  # Total number of observations
#         df_between = k - 1
#         df_within = N - k
#         f_statistic, p_value = stats.f_oneway(data_sendRate[5][operation][folder], data_sendRate[10][operation][folder], data_sendRate[20][operation][folder], data_sendRate[50][operation][folder])
#         f_critical = stats.f.ppf(1 - 0.05, df_between, df_within)
#         #Print the results
#         # print(f"F-Statistic for {folder} {operation}:", round(f_statistic,2))
#         print(f"for {folder} solution for {operation} operation at different sendRate")
#         # print("Degrees of freedom (between):", df_between)
#         # print("Degrees of freedom (within):", df_within)
#         # print("F critical value:", round(f_critical,4))
#         posthoc = stats.tukey_hsd(data_sendRate[5][operation][folder], data_sendRate[10][operation][folder], data_sendRate[20][operation][folder], data_sendRate[50][operation][folder])
#         print(posthoc)