import matplotlib.pyplot as plt
import numpy as np
import statistics

def plot_graph_2(dataset):

    #keys stand for rank spread
    rank_spread = {1: {'image_object':[],'javascript_object':[],'css_object':[],'flash_object':[]},
                   2: {'image_object':[],'javascript_object':[],'css_object':[],'flash_object':[]},
                   3: {'image_object':[],'javascript_object':[],'css_object':[],'flash_object':[]},
                   4: {'image_object':[],'javascript_object':[],'css_object':[],'flash_object':[]},
                   5: {'image_object':[],'javascript_object':[],'css_object':[],'flash_object':[]}}
    for site in dataset:

        if site[1]==1:
            rank_spread[1]['image_object'].append(site[2])
            rank_spread[1]['javascript_object'].append(site[3])
            rank_spread[1]['css_object'].append(site[4])
            rank_spread[1]['flash_object'].append(site[5])

        elif site[1]==2:
            rank_spread[2]['image_object'].append(site[2])
            rank_spread[2]['javascript_object'].append(site[3])
            rank_spread[2]['css_object'].append(site[4])
            rank_spread[2]['flash_object'].append(site[5])

        elif site[1]==3:
            rank_spread[3]['image_object'].append(site[2])
            rank_spread[3]['javascript_object'].append(site[3])
            rank_spread[3]['css_object'].append(site[4])
            rank_spread[3]['flash_object'].append(site[5])

        elif site[1]==4:
            rank_spread[4]['image_object'].append(site[2])
            rank_spread[4]['javascript_object'].append(site[3])
            rank_spread[4]['css_object'].append(site[4])
            rank_spread[4]['flash_object'].append(site[5])

        elif site[1]==5:
            rank_spread[5]['image_object'].append(site[2])
            rank_spread[5]['javascript_object'].append(site[3])
            rank_spread[5]['css_object'].append(site[4])
            rank_spread[5]['flash_object'].append(site[5])

    #sort the lists according to find the median
    rank_spread[1]['image_object'].sort()
    rank_spread[1]['javascript_object'].sort()
    rank_spread[1]['css_object'].sort()
    rank_spread[1]['flash_object'].sort()

    rank_spread[2]['image_object'].sort()
    rank_spread[2]['javascript_object'].sort()
    rank_spread[2]['css_object'].sort()
    rank_spread[2]['flash_object'].sort()

    rank_spread[3]['image_object'].sort()
    rank_spread[3]['javascript_object'].sort()
    rank_spread[3]['css_object'].sort()
    rank_spread[3]['flash_object'].sort()

    rank_spread[4]['image_object'].sort()
    rank_spread[4]['javascript_object'].sort()
    rank_spread[4]['css_object'].sort()
    rank_spread[4]['flash_object'].sort()

    rank_spread[5]['image_object'].sort()
    rank_spread[5]['javascript_object'].sort()
    rank_spread[5]['css_object'].sort()
    rank_spread[5]['flash_object'].sort()

    #creating the graph
    rank_cat = ("1-400", "401-1k", "1001-2.5k", "5k-10k", "10001-20k")
    x_pos = np.arange(len(rank_cat))
    colors = ['#624ea7', 'g', 'yellow', 'k', 'maroon']

    #image graph
    median_objects=[statistics.median(rank_spread[1]['image_object']),
                   statistics.median(rank_spread[2]['image_object']),
                   statistics.median(rank_spread[3]['image_object']),
                   statistics.median(rank_spread[4]['image_object']),
                   statistics.median(rank_spread[5]['image_object'])]

    plt.bar(x_pos, median_objects, align='center', alpha=0.5,color=colors)
    plt.xticks(x_pos, rank_cat)
    plt.ylabel('Median No. of Objects')
    plt.title('Image')
    plt.show()

    #javascript
    median_objects = [statistics.median(rank_spread[1]['javascript_object']),
                      statistics.median(rank_spread[2]['javascript_object']),
                      statistics.median(rank_spread[3]['javascript_object']),
                      statistics.median(rank_spread[4]['javascript_object']),
                      statistics.median(rank_spread[5]['javascript_object'])]
    plt.bar(x_pos, median_objects, align='center', alpha=0.5,color=colors)
    plt.xticks(x_pos, rank_cat)
    plt.ylabel('Median No. of Objects')
    plt.title('Javascript')
    plt.show()
   #CSS
    median_objects = [statistics.median(rank_spread[1]['css_object']),
                      statistics.median(rank_spread[2]['css_object']),
                      statistics.median(rank_spread[3]['css_object']),
                      statistics.median(rank_spread[4]['css_object']),
                      statistics.median(rank_spread[5]['css_object'])]
    plt.bar(x_pos, median_objects, align='center', alpha=0.5,color=colors)
    plt.xticks(x_pos, rank_cat)
    plt.ylabel('Median No. of Objects')
    plt.title('CSS')
    plt.show()
    #flash
    median_objects = [statistics.median(rank_spread[1]['flash_object']),
                      statistics.median(rank_spread[2]['flash_object']),
                      statistics.median(rank_spread[3]['flash_object']),
                      statistics.median(rank_spread[4]['flash_object']),
                      statistics.median(rank_spread[5]['flash_object'])]
    plt.bar(x_pos, median_objects, align='center', alpha=0.5,color=colors)
    plt.xticks(x_pos, rank_cat)
    plt.ylabel('Median No. of Objects')
    plt.title('Flash')
    plt.show()
    return 0
