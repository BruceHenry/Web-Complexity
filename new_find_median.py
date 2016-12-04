import csv


def median_site(dataset):
    # image median
    median = {"image": 0, "js": 0, "css": 0, "flash": 0, "xml": 0, "html": 0, "json": 0, "video": 0, "other": 0}
    median_name = ("image", "js", "css", "flash", "xml", "html", "json", "video", "other")
    count = 0

    for key in median_name:
        sort = sorted(dataset, key=lambda tup: tup[count])
        length = len(sort)
        if length % 2 == 0:
            median[key] = (sort[length // 2 - 1][count] + sort[length // 2][count]) / 2
        else:
            median[key] = sort[length // 2][count]
        count += 1
    median_site = []

    index = []
    for site in dataset:
        flag = 1
        for i in range(len(median_name)):
            if abs(site[i] - median[median_name[i]]) < 3:
                continue
            else:
                flag = 0
        if flag == 1:
            median_site.append(site)
            index.append(dataset.index(site))
    return index, median_site


dataset = []
non_origin_object = []
non_origin_byte = []
origin_object = []

with open("data.csv") as tsvfile:
    csvreader = csv.reader(tsvfile)  # , delimiter="\t"
    for line in csvreader:
        dataset.append([int(float(line[27])), int(float(line[28])), int(float(line[29])), int(float(line[30])),
                        int(float(line[31])), int(float(line[32])), int(float(line[33])), int(float(line[34])),
                        int(float(line[58]))])

count = 0
with open("data.csv") as tsvfile:
    csvreader = csv.reader(tsvfile)
    index, non_origin_object = median_site(dataset)
    count = 0
    for element in index:
        for line in csvreader:
            if count == element:
                non_origin_byte.append(
                    [int(float(line[35])), int(float(line[36])), int(float(line[37])), int(float(line[38])),
                     int(float(line[39])), int(float(line[40])), int(float(line[41])), int(float(line[42])),
                     int(float(line[59]))])
                origin_object.append(
                    [int(float(line[3]) - float(line[27])), int(float(line[4]) - float(line[28])),
                     int(float(line[5]) - float(line[29])), int(float(line[6]) - float(line[30])),
                     int(float(line[7]) - float(line[31])), int(float(line[8]) - float(line[32])),
                     int(float(line[9]) - float(line[33])), int(float(line[10]) - float(line[34])),
                     int(float(line[60]) - float(line[58]))])
            count += 1

print(non_origin_object)
print(non_origin_byte)
print(origin_object)
