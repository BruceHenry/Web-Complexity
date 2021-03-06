import matplotlib.pyplot as plt
import numpy as np
import statistics
import csv

dataset = []

with open("data.csv") as tsvfile:
    reader = csv.reader(tsvfile)
    for line in reader:
        dataset.append(
            [int(line[1]), line[2], int(float(line[3])), int(float(line[4])), int(float(line[5])), int(float(line[6])),
             int(float(line[11])), int(float(line[12])), int(float(line[13])), int(float(line[14])),
             int(float(line[52]))])

#print(dataset)
# keys stand for rank spreadd
rank_spread = {1: {'image_object': [], 'javascript_object': [], 'css_object': [], 'flash_object': []},
               2: {'image_object': [], 'javascript_object': [], 'css_object': [], 'flash_object': []},
               3: {'image_object': [], 'javascript_object': [], 'css_object': [], 'flash_object': []},
               4: {'image_object': [], 'javascript_object': [], 'css_object': [], 'flash_object': []},
               5: {'image_object': [], 'javascript_object': [], 'css_object': [], 'flash_object': []}}
for site in dataset:
    if site[0] == 1:
        rank_spread[1]['image_object'].append(site[2])
        rank_spread[1]['javascript_object'].append(site[3])
        rank_spread[1]['css_object'].append(site[4])
        rank_spread[1]['flash_object'].append(site[5])

    elif site[0] == 2:
        rank_spread[2]['image_object'].append(site[2])
        rank_spread[2]['javascript_object'].append(site[3])
        rank_spread[2]['css_object'].append(site[4])
        rank_spread[2]['flash_object'].append(site[5])

    elif site[0] == 3:
        rank_spread[3]['image_object'].append(site[2])
        rank_spread[3]['javascript_object'].append(site[3])
        rank_spread[3]['css_object'].append(site[4])
        rank_spread[3]['flash_object'].append(site[5])

    elif site[0] == 4:
        rank_spread[4]['image_object'].append(site[2])
        rank_spread[4]['javascript_object'].append(site[3])
        rank_spread[4]['css_object'].append(site[4])
        rank_spread[4]['flash_object'].append(site[5])

    elif site[0] == 5:
        rank_spread[5]['image_object'].append(site[2])
        rank_spread[5]['javascript_object'].append(site[3])
        rank_spread[5]['css_object'].append(site[4])
        rank_spread[5]['flash_object'].append(site[5])

fig = plt.figure(figsize=(12, 12))
# creating the graph
rank_cat = ("1-400", "401-1k", "1001-2.5k", "5k-10k", "10001-20k")
x_pos = np.arange(len(rank_cat))
colors = ['#624ea7', 'g', 'yellow', 'k', 'maroon']

# image graph
median_objects = [statistics.median(rank_spread[1]['image_object']),
                  statistics.median(rank_spread[2]['image_object']),
                  statistics.median(rank_spread[3]['image_object']),
                  statistics.median(rank_spread[4]['image_object']),
                  statistics.median(rank_spread[5]['image_object'])]
sub = fig.add_subplot(221)
sub.bar(x_pos, median_objects, align='center', alpha=0.7, color=colors)
sub.set_xticks(x_pos)
sub.set_xticklabels(rank_cat, rotation=60)
sub.set_ylabel('Median No. of Objects')
sub.set_title('Image')

# javascript
median_objects = [statistics.median(rank_spread[1]['javascript_object']),
                  statistics.median(rank_spread[2]['javascript_object']),
                  statistics.median(rank_spread[3]['javascript_object']),
                  statistics.median(rank_spread[4]['javascript_object']),
                  statistics.median(rank_spread[5]['javascript_object'])]
sub = fig.add_subplot(222)
sub.bar(x_pos, median_objects, align='center', alpha=0.7, color=colors)
sub.set_xticks(x_pos)
sub.set_xticklabels(rank_cat, rotation=60)
sub.set_ylabel('Median No. of Objects')
sub.set_title('Javascript')
# CSS
median_objects = [statistics.median(rank_spread[1]['css_object']),
                  statistics.median(rank_spread[2]['css_object']),
                  statistics.median(rank_spread[3]['css_object']),
                  statistics.median(rank_spread[4]['css_object']),
                  statistics.median(rank_spread[5]['css_object'])]
sub = fig.add_subplot(223)
sub.bar(x_pos, median_objects, align='center', alpha=0.7, color=colors)
sub.set_xticks(x_pos)
sub.set_xticklabels(rank_cat, rotation=60)
sub.set_ylabel('Median No. of Objects')
sub.set_title('CSS')

# flash
median_objects = [statistics.median(rank_spread[1]['flash_object']),
                  statistics.median(rank_spread[2]['flash_object']),
                  statistics.median(rank_spread[3]['flash_object']),
                  statistics.median(rank_spread[4]['flash_object']),
                  statistics.median(rank_spread[5]['flash_object'])]
sub = fig.add_subplot(224)
sub.bar(x_pos, median_objects, align='center', alpha=0.7, color=colors)
sub.set_xticks(x_pos)
sub.set_ylim([0, 5])
sub.set_xticklabels(rank_cat, rotation=60)
sub.set_ylabel('Median No. of Objects')
sub.set_title('flash')

fig.subplots_adjust(hspace=.5)
plt.show()

# category to number of objects
categories = (
    "newsandmedia", "business", "shopping", "education", "entertainment", "informationtech", "adult", "other")
categories_name = (
    "news & media", "business", "shopping", "education", "entertainment", "information & tech", "adult", "other")
graph = ["image", "javascript", "CSS", "flash"]
fig = plt.figure(figsize=(12, 12))
plots = [221, 222, 223, 224]
for j in range(0, 4):
    x = [[], [], [], [], [], [], [], []]
    colors = []
    cmap = plt.get_cmap('jet')
    colors = cmap(np.linspace(0, 1.0, len(categories)))
    for site in dataset:
        ca = site[1]
        if ca not in categories:
            if ca in ['sports', "travel", "streamingmedia"]:
                ca = "entertainment"
            else:
                ca = "other"
            if site[len(site) - 1] == 0:
                continue
        x[categories.index(ca)].append(site[2 + j])


    x_pos = np.arange(len(categories))
    median_objects = []
    for i in range(len(x)):
        median_objects.append(statistics.median(x[i]))
    sub = fig.add_subplot(plots[j])
    if j == 3:
        sub.set_ylim([0, 5])
    sub.bar(x_pos, median_objects, align='center', alpha=0.7, color=colors)
    sub.set_xticks(x_pos)
    sub.set_xticklabels(categories_name, rotation=70)
    sub.set_ylabel('Median No. of Objects')
    sub.set_title(graph[j])
fig.subplots_adjust(hspace=.5)
plt.show()

# category to total bytes downloaded
count = 0
fig = plt.figure(figsize=(12, 12))
plots = [221, 222, 223, 224]
for j in range(0, 4):
    x = [[], [], [], [], [], [], [], []]
    for site in dataset:
        ca = site[1]
        if ca not in categories:
            if ca in ['sports', "travel", "streamingmedia"]:
                ca = "entertainment"
            else:
                ca = "other"
        if site[len(site) - 1] == 0:
            count += 1
            continue
        x[categories.index(ca)].append(int(float(site[6 + j])) / float(site[len(site) - 1]))
        #print(ca)
    x_pos = np.arange(len(categories))
    median_objects = []
    print(x)
    for i in range(len(x)):
        median_objects.append(statistics.median(x[i]))

    sub = fig.add_subplot(plots[j])
    if j == 3:
        sub.set_ylim([0, 5])
    sub.bar(x_pos, median_objects, align='center', alpha=0.7, color=colors)
    sub.set_xticks(x_pos)
    sub.set_xticklabels(categories_name, rotation=70)
    sub.set_ylabel('Total % of byte downloaded')
    sub.set_title(graph[j])

fig.subplots_adjust(hspace=.5)
plt.show()
