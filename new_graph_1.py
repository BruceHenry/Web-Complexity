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


def graph_1_rank(dataset):
    x = [[], [], [], [], []]
    y = [[], [], [], [], []]
    rank_cat = ("1-400", "401-1k", "1001-2.5k", "5k-10k", "10001-20k")
    for site in dataset:
        x[site[1] - 1].append(site[2])
    print(x)
    print(y)
    n = 0
    fig, ax = plt.subplots()
    while n < 5:
        x[n].sort()
        for element in x[n]:
            y[n].append(fraction(x[n], element))
        ax.plot(x[n], y[n], label=rank_cat[n])
        n += 1

    legend = ax.legend(loc='lower right', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.90')

    for label in legend.get_texts():
        label.set_fontsize('large')

    for label in legend.get_lines():
        label.set_linewidth(1.5)  # the legend line width

    plt.figure(1)
    plt.yscale('linear')
    plt.title('linear')
    plt.grid(True)
    plt.show()


def graph_1_category(dataset):
    x = [[], [], [], [], [], [], [], [], [], [], [], []]
    y = [[], [], [], [], [], [], [], [], [], [], [], []]
    categories = (
        "newsandmedia", "business", "shopping", "education", "entertainment", "sports", "travel", "informationtech",
        "streamingmedia", "health", "adult", "other")
    for site in dataset:
        ca = site[0]
        if ca not in categories:
            ca = "other"
        x[categories.index(ca)].append(site[2])
    print(x)
    print(y)
    n = 0
    fig, ax = plt.subplots()
    cmap = plt.get_cmap('jet')
    colors = cmap(np.linspace(0, 1.0, len(categories)))

    while n < 12:
        x[n].sort()
        for element in x[n]:
            y[n].append(fraction(x[n], element))
        # ax.plot(x[n], y[n], label=categories[n])
        n += 1

    n = 0
    for color in colors:
        ax.plot(x[n], y[n], label=categories[n], color=color)
        n += 1

    legend = ax.legend(loc='lower right', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.90')

    for label in legend.get_texts():
        label.set_fontsize('large')

    for label in legend.get_lines():
        label.set_linewidth(3)  # the legend line width

    plt.figure(1)
    plt.yscale('linear')
    plt.title('linear')
    plt.grid(True)
    plt.show()


dataset = []
with open("data.csv") as tsvfile:
    csvreader = csv.reader(tsvfile, delimiter="\t")
    for line in csvreader:
        dataset.append([line[0], int(line[1]), int(line[61])])
graph_1_rank(dataset)
graph_1_category(dataset)