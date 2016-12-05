import csv
import matplotlib.pyplot as plt
import numpy as np


def fraction(d, value):
    count = 0
    for element in d:
        if element <= value:
            count += 1
        else:
            break
    return count / len(d)


def graph_13(dataset1, dataset2):
    x = [[], []]
    y = [[], []]
    rank_cat = ("Median", "90%th Lie")
    for site in dataset1:
        x[0].append(site)
    for site in dataset2:
        x[1].append(site)

    n = 0
    fig, ax = plt.subplots()
    while n < 2:
        x[n].sort()
        for element in x[n]:
            y[n].append(fraction(x[n], element))
        x[n] = [0.0] + x[n]
        y[n] = [0.0] + y[n]
        ax.plot(x[n], y[n], label=rank_cat[n], linewidth=3.0)
        n += 1

    legend = ax.legend(loc='lower right', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.90')

    for label in legend.get_texts():
        label.set_fontsize('large')

    for label in legend.get_lines():
        label.set_linewidth(3)  # the legend line width

    plt.figure(1)
    #plt.xlim(0, 450)
    plt.yscale('linear')
    plt.grid(True)
    plt.show()



dataset1 = []
with open("data.csv") as tsvfile:
    csvreader = csv.reader(tsvfile)  # , delimiter="\t"
    for line in csvreader:
        # category name, rank range, total object number
        dataset1.append(int(float(line[51])/1000))

dataset2 = []
with open("90th_data.csv") as tsvfile:
    csvreader = csv.reader(tsvfile)  # , delimiter="\t"
    for line in csvreader:
        # category name, rank range, total object number
        dataset2.append(int(float(line[51])/1000))

graph_13(dataset1, dataset2)
