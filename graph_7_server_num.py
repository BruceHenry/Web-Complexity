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


def graph_7_rank(dataset):
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
        x[n] = [0.0] + x[n]
        y[n] = [0.0] + y[n]
        ax.plot(x[n], y[n], label=rank_cat[n], linewidth=2.0)
        n += 1

    legend = ax.legend(loc='lower right', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.90')

    for label in legend.get_texts():
        label.set_fontsize('large')

    for label in legend.get_lines():
        label.set_linewidth(3)  # the legend line width

    plt.figure(1)
    plt.xlim(0, 200)
    plt.yscale('linear')
    plt.title('Num of servers by rank')
    plt.grid(True)
    plt.show()


def graph_7_category(dataset):
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
        x[categories.index(ca)].append(site[2])
    print(x)
    print(y)
    n = 0
    fig, ax = plt.subplots()
    cmap = plt.get_cmap('jet')
    colors = cmap(np.linspace(0, 1.0, len(categories)))

    while n < 8:
        x[n].sort()
        for element in x[n]:
            y[n].append(fraction(x[n], element))
        # ax.plot(x[n], y[n], label=categories[n])
        n += 1

    n = 0
    for color in colors:
        x[n] = [0.0] + x[n]
        y[n] = [0.0] + y[n]
        ax.plot(x[n], y[n], label=categories[n], color=color, linewidth=2.0)
        n += 1

    legend = ax.legend(loc='lower right', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.90')

    for label in legend.get_texts():
        label.set_fontsize('large')

    for label in legend.get_lines():
        label.set_linewidth(3)  # the legend line width

    plt.figure(1)
    plt.xlim(0, 200)
    plt.yscale('linear')
    plt.title('Num of servers by category')
    plt.grid(True)
    plt.show()


dataset = []
with open("data.csv") as tsvfile:
    csvreader = csv.reader(tsvfile)  # , delimiter="\t"
    for line in csvreader:
        # category name, rank range, number of servers:len(host)
        dataset.append([line[2], int(float(line[1])), int(float(line[57]))])
graph_7_rank(dataset)
graph_7_category(dataset)
