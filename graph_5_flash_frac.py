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


def graph_5(dataset):
    x = [[], [], [], [], [], [], [], []]
    y = [[], [], [], [], [], [], [], []]
    categories = (
        "newsandmedia", "business", "shopping", "education", "entertainment", "informationtech", "adult", "other")
    for site in dataset:
        ca = site[0]
        if ca not in categories:
            if ca in ['sports', "travel", "streamingmedia"]:
                ca = "entertainment"
            else:
                ca = "other"
        x[categories.index(ca)].append(site[1])
    n = 0
    fig, ax = plt.subplots()
    # cmap = plt.get_cmap('jet')
    # colors = cmap(np.linspace(0, 1.0, len(categories)))

    count = 0
    while n < 8:
        x[n].sort()
        for element in x[n]:
            y[n].append(fraction(x[n], element))
        if len(x[n]) != 0:
            count += 1
        n += 1

    cmap = plt.get_cmap('jet')
    colors = cmap(np.linspace(0, 1.0, count))

    n = 0
    for color in colors:
        while len(x[n]) == 0:
            n += 1
        x[n] = [0.0] + x[n]
        y[n] = [0.0] + y[n]
        ax.plot(x[n], y[n], label=categories[n], color=color, linewidth=2.0)
        n += 1
    # print(x)
    # print(y)
    legend = ax.legend(loc='lower right', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.90')

    for label in legend.get_texts():
        label.set_fontsize('large')

    for label in legend.get_lines():
        label.set_linewidth(3)  # the legend line width

    plt.figure(1)
    plt.xlim(0, 0.02)
    plt.yscale('linear')
    plt.title('Median Fraction of Flash Objects by Category')
    plt.grid(True)
    plt.show()


dataset = []
with open("data.csv") as tsvfile:
    csvreader = csv.reader(tsvfile)  # , delimiter="\t"
    for line in csvreader:
        if int(float(line[6])) != 0:
            sum = float(line[3]) + float(line[4]) + float(line[5]) + float(line[6]) + float(line[7]) + float(
                line[8]) + float(line[9]) + float(line[10]) + float(line[60])
            dataset.append([line[2], (float(line[6]) / sum)])

graph_5(dataset)
