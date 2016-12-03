import csv
import matplotlib.pyplot as plt
import numpy as np


def time_object_figure(dataset):
    max_num = 50
    data = []

    n = 0
    while n < max_num:
        data.append([])
        n += 1

    for site in dataset:
        index = site[1] // 10
        if index < max_num - 1:
            data[index].append(site[0] / 1000)
        else:
            data[max_num - 1].append(site[0] / 1000)

    x_axis_name = np.arange(10, max_num * 10 - 1, 10)
    fig, ax1 = plt.subplots(figsize=(20, 10))
    plt.boxplot(data)
    x_tick_names = plt.setp(ax1, xticklabels=x_axis_name)
    plt.setp(x_tick_names, fontsize=10)
    plt.ylim(0, 60)
    ax1.set_title('RenderEnd and number of object', loc="left", fontsize=15)
    ax1.set_xlabel('Number of Objects', fontsize=18)
    ax1.set_ylabel('Load Time(s)', fontsize=18)
    plt.show()


dataset = []
with open("data.csv") as tsvfile:
    csvreader = csv.reader(tsvfile)# , delimiter="\t"
    for line in csvreader:
        # total["loadTime"], total["request"]
        dataset.append([int(float(line[51])), int(float(line[53]))])
time_object_figure(dataset)
