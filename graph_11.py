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


def graph_11_rank(dataset):
    x = [[], [], [], [], [], [], [], []]
    y = [[], [], [], [], [], [], [], []]
    categories = ("image", "javascript", "css", "flash", "xml", "html", "JSON", "video")
    for site in dataset:
        for element in site[:8]:
            if element > 0:
                x[site.index(element)].append(element)
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
        n += 1

    n = 0
    for color in colors:
        x[n] = [0.0] + x[n]
        y[n] = [0.0] + y[n]
        ax.plot(x[n], y[n], label=categories[n], color=color, linewidth=2.5)
        n += 1

    legend = ax.legend(loc='lower right', shadow=True)
    frame = legend.get_frame()
    frame.set_facecolor('0.90')

    for label in legend.get_texts():
        label.set_fontsize('large')

    for label in legend.get_lines():
        label.set_linewidth(3)  # the legend line width

    plt.figure(1)
    #plt.xlim(0, 20)
    plt.xscale('log')
    plt.yscale('linear')
    plt.title('Number of objects requests')
    plt.grid(True)
    plt.show()


def graph_11_category(dataset):
    x = [[], [], [], [], [], [], [], []]
    y = [[], [], [], [], [], [], [], []]
    categories = ("image", "javascript", "css", "flash", "xml", "html", "JSON", "video")
    for site in dataset:
        for element in site[8:16]:
            if element > 0:
                x[site.index(element)-8].append(element)
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
        n += 1

    n = 0
    for color in colors:
        x[n] = [0.0] + x[n]
        y[n] = [0.0] + y[n]
        ax.plot(x[n], y[n], label=categories[n], color=color, linewidth=3.0)
        n += 1

    legend = ax.legend(loc='lower right')
    frame = legend.get_frame()
    frame.set_facecolor('0.90')

    for label in legend.get_texts():
        label.set_fontsize('x-small')

    for label in legend.get_lines():
        label.set_linewidth(3)  # the legend line width

    plt.figure(1)
    #plt.xlim(0, 20)
    plt.xscale('log')
    plt.yscale('linear')
    plt.title('Median size')
    plt.grid(True)
    plt.show()


dataset = []
with open("data.csv") as tsvfile:
    csvreader = csv.reader(tsvfile)  # , delimiter="\t"
    for line in csvreader:
        # image, javascript, css, flash, xml, html, Json, video
        dataset.append([float(line[27]), float(line[28]), float(line[29]), float(line[30]), float(line[31]), float(
            line[32]), float(line[33]), float(line[34]), float(line[35]), float(line[36]), float(line[37]),
                        float(line[38]), float(line[39]), float(line[40]), float(line[41]), float(line[42])])
#graph_11_rank(dataset)
graph_11_category(dataset)
