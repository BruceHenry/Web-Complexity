import json
import os
import re
import dns.resolver
import csv
import statistics


def get_host(url):
    pattern_dns = re.compile('co\0|edu\0|com\0')
    s = url.split('.')
    if len(s) < 3:
        s = s[len(s) - 2] + '.' + s[len(s) - 1]
        return s
    if pattern_dns.match(s[len(s) - 2]):
        s = s[len(s) - 3] + '.' + s[len(s) - 2] + '.' + s[len(s) - 1]
    else:
        s = s[len(s) - 2] + '.' + s[len(s) - 1]
    return s


def find_rank_range(rank):
    if rank <= 400:
        return 1
    elif rank <= 1000:
        return 2
    elif rank <= 2500:
        return 3
    elif rank <= 10000:
        return 4
    elif rank <= 20000:
        return 5


# path = "/home/kartik/Documents/untitled folder/"
# path = "D:/harsample/untitled folder/"
path = "M:/hardata/"
dirs = os.listdir(path)
pattern_har = re.compile(".*.har")
i = 1

rank_dict = {}
with open("ranklist") as tsvfile:
    tsvreader = csv.reader(tsvfile, delimiter="\t")
    for line in tsvreader:
        try:
            rank_dict[line[1]] = int(line[0])
        except:
            continue

categories = {}
with open("mapper.txt") as catfile:
    catreader = csv.reader(catfile, delimiter="\t")
    for line in catreader:
        try:
            categories[line[0]] = line[1]
        except:
            continue

# for x in categories:
#     x_values = []
#     x_values.append(x)
#     x_values.append(categories[x])
#     with open("datatest.csv", 'a') as f:
#         writer = csv.writer(f, dialect='excel')
#         writer.writerow(x_values)
# print(categories)
site = {}
serverCache = {}
rank_spread = {"1-400": {}, "400-1000": {}, "1000-2500": {}, "5000-10000": {}, "10000-20000": {}}
image_type = {}
for file in dirs:
    if pattern_har.match(file):
        file = path + file
        with open(file, 'rb') as f:
            try:
                data = json.loads(f.read().decode("utf-8-sig"))
            except:
                continue
        #print(file)

        host = []
        ca = ""
        try:
            host.append(data['log']['entries'][0]['request']["headers"][0]['value'])
            host[0] = get_host(host[0])
            url = "http://www." + host[0]
            rank = rank_dict[host[0]]
        except:
            continue

        if categories.get(url, 0) == 0:
            continue
        else:
            ca = categories[url]

        #print("Host Name:", host[0], "  Category:", ca, "  URL:", url)

        nameServers = []
        if serverCache.get(host[0], 0) == 0:
            try:
                serverCache[host[0]] = dns.resolver.query(host[0], "NS")
            except:
                continue
        # answer = dns.resolver.query(get_host(host[0]), "NS")
        # print("serverCache", serverCache)
        for nameServer in serverCache[host[0]]:
            nameServers.append(str(nameServer)[:len(str(nameServer)) - 1])
        #print("nameServers:", nameServers)

        originServerNumber = 1
        total = {"request": 0, "size": 0, "loadTime": 0}
        non_origin_total = {"object": 0, "size": 0, "loadTime": 0}
        css = {"object": 0, "size": 0, "loadTime": 0, "n_object": 0, "n_size": 0, "n_loadTime": 0}
        image = {"object": 0, "size": 0, "loadTime": 0, "n_object": 0, "n_size": 0, "n_loadTime": 0}
        flash = {"object": 0, "size": 0, "loadTime": 0, "n_object": 0, "n_size": 0, "n_loadTime": 0}
        javascript = {"object": 0, "size": 0, "loadTime": 0, "n_object": 0, "n_size": 0, "n_loadTime": 0}
        xml = {"object": 0, "size": 0, "loadTime": 0, "n_object": 0, "n_size": 0, "n_loadTime": 0}
        html = {"object": 0, "size": 0, "loadTime": 0, "n_object": 0, "n_size": 0, "n_loadTime": 0}
        Json = {"object": 0, "size": 0, "loadTime": 0, "n_object": 0, "n_size": 0, "n_loadTime": 0}
        video = {"object": 0, "size": 0, "loadTime": 0, "n_object": 0, "n_size": 0, "n_loadTime": 0}
        other = {"object": 0, "size": 0, "loadTime": 0, "n_object": 0, "n_size": 0, "n_loadTime": 0}

        pattern_image = re.compile('image.*')
        pattern_css = re.compile("text/css.*")
        pattern_javascript = re.compile('text/.*javascript|application/.*script')
        pattern_xml = re.compile('test/xml.*|application/xml.*')
        pattern_html = re.compile('text/html.*')
        pattern_json = re.compile('application/json.*|text/.*json')
        pattern_video = re.compile('video.*')
        pattern_response = re.compile("2.*")

        total["request"] = len(data['log']['entries'])
        total["loadTime"] = data['log']['pages'][0]['pageTimings']['onLoad']
        if total["loadTime"] <= 0:
            continue

        for entry in data['log']['entries']:

            find_flag = 0  # 0 means non-origin, 1 means origin.

            try:
                if entry['request']["headers"][0]['value'] not in host:
                    host.append(entry['request']["headers"][0]['value'])
                    if serverCache.get(get_host(host[len(host) - 1]), 0) == 0:
                        try:
                            serverCache[get_host(host[len(host) - 1])] = dns.resolver.query(
                                get_host(host[len(host) - 1]), "NS")
                        except:
                            continue
                    # answer = dns.resolver.query(get_host(host[len(host) - 1]), "NS")
                    for ns in serverCache[get_host(host[len(host) - 1])]:
                        if str(ns)[:len(str(ns)) - 1] in nameServers:
                            originServerNumber += 1
                            find_flag = 1
                            break
                    if find_flag == 0:
                        non_origin_total["object"] += 1
                        non_origin_total["size"] += entry['response']['content']['size']
                        non_origin_total["loadTime"] += entry['time']
            except:
                pass

            total["size"] += entry['response']['content']['size']
            # total["loadTime"] += entry['time']

            if (pattern_image.match(entry['response']['content']['mimeType']) and pattern_response.match(
                    str(entry['response']['status']))):
                if entry['response']['content']['mimeType'] not in image_type:
                    image_type[entry['response']['content']['mimeType']] = 1
                else:
                    image_type[entry['response']['content']['mimeType']] += 1
                image["object"] += 1
                image["size"] += entry['response']['content']['size']
                image["loadTime"] += entry['time']
                if find_flag == 0:
                    image["n_object"] += 1
                    image["n_size"] += entry['response']['content']['size']
                    image["n_loadTime"] += entry['time']
            elif (pattern_css.match(entry['response']['content']['mimeType']) and pattern_response.match(
                    str(entry['response']['status']))):
                css["object"] += 1
                css["size"] += entry['response']['content']['size']
                css["loadTime"] += entry['time']
                if find_flag == 0:
                    css["n_object"] += 1
                    css["n_size"] += entry['response']['content']['size']
                    css["n_loadTime"] += entry['time']
            elif (entry['response']['content'][
                      'mimeType'] == 'application/x-shockwave-flash' and pattern_response.match(
                str(entry['response']['status']))):
                flash["object"] += 1
                flash["size"] += entry['response']['content']['size']
                flash["loadTime"] += entry['time']
                if find_flag == 0:
                    flash["n_object"] += 1
                    flash["n_size"] += entry['response']['content']['size']
                    flash["n_loadTime"] += entry['time']
            elif (pattern_javascript.match(entry['response']['content']['mimeType']) and pattern_response.match(
                    str(entry['response']['status']))):
                javascript["object"] += 1
                javascript["size"] += entry['response']['content']['size']
                javascript["loadTime"] += entry['time']
                if find_flag == 0:
                    javascript["n_object"] += 1
                    javascript["n_size"] += entry['response']['content']['size']
                    javascript["n_loadTime"] += entry['time']
            elif (pattern_xml.match(entry['response']['content']['mimeType']) and pattern_response.match(
                    str(entry['response']['status']))):
                xml["object"] += 1
                xml["size"] += entry['response']['content']['size']
                xml["loadTime"] += entry['time']
                if find_flag == 0:
                    xml["n_object"] += 1
                    xml["n_size"] += entry['response']['content']['size']
                    xml["n_loadTime"] += entry['time']
            elif (pattern_html.match(entry['response']['content']['mimeType']) and pattern_response.match(
                    str(entry['response']['status']))):
                html["object"] += 1
                html["size"] += entry['response']['content']['size']
                html["loadTime"] += entry['time']
                if find_flag == 0:
                    html["n_object"] += 1
                    html["n_size"] += entry['response']['content']['size']
                    html["n_loadTime"] += entry['time']
            elif (pattern_json.match(entry['response']['content']['mimeType']) and pattern_response.match(
                    str(entry['response']['status']))):
                Json["object"] += 1
                Json["size"] += entry['response']['content']['size']
                Json["loadTime"] += entry['time']
                if find_flag == 0:
                    Json["n_object"] += 1
                    Json["n_size"] += entry['response']['content']['size']
                    Json["n_loadTime"] += entry['time']
            elif (pattern_video.match(entry['response']['content']['mimeType']) and pattern_response.match(
                    str(entry['response']['status']))):
                video["object"] += 1
                video["size"] += entry['response']['content']['size']
                video["loadTime"] += entry['time']
                if find_flag == 0:
                    video["n_object"] += 1
                    video["n_size"] += entry['response']['content']['size']
                    video["n_loadTime"] += entry['time']
            elif pattern_response.match(str(entry['response']['status'])):
                other["object"] += 1
                other["size"] += entry['response']['content']['size']
                other["loadTime"] += entry['time']
                if find_flag == 0:
                    other["n_object"] += 1
                    other["n_size"] += entry['response']['content']['size']
                    other["n_loadTime"] += entry['time']

        if total["size"] == 0:
            continue

        # print("hostName:", get_host(host[0]), "rank:", rank_dict[host[0]])
        # print("Number of servers:", len(host))
        # print("originServerNumber:", originServerNumber)
        # print("non_origin_total:", non_origin_total)
        # print("servers:", host)
        # print('total:', total)
        # print('image:', image)
        # print('css:', css)
        # print('flash:', flash)
        # print('javascript:', javascript)
        # print('xml:', xml)
        # print('html:', html)
        # print('json:', Json)
        # print('video:', video)
        # print(i)
        i += 1

        if rank <= 400:
            cat = 1
            if rank_spread["1-400"].get(host[0], 0) == 0:
                rank_spread["1-400"][host[0]] = 1
            else:
                rank_spread["1-400"][host[0]] += 1
        elif rank <= 1000:
            cat = 2
            if rank_spread["400-1000"].get(host[0], 0) == 0:
                rank_spread["400-1000"][host[0]] = 1
            else:
                rank_spread["400-1000"][host[0]] += 1
        elif rank <= 2500:
            cat = 3
            if rank_spread["1000-2500"].get(host[0], 0) == 0:
                rank_spread["1000-2500"][host[0]] = 1
            else:
                rank_spread["1000-2500"][host[0]] += 1
        elif rank <= 10000:
            cat = 4
            if rank_spread["5000-10000"].get(host[0], 0) == 0:
                rank_spread["5000-10000"][host[0]] = 1
            else:
                rank_spread["5000-10000"][host[0]] += 1
        elif rank <= 20000:
            cat = 5
            if rank_spread["10000-20000"].get(host[0], 0) == 0:
                rank_spread["10000-20000"][host[0]] = 1
            else:
                rank_spread["10000-20000"][host[0]] += 1

        row_values = [
            image["object"], javascript["object"], css["object"], flash["object"], xml["object"],
            html["object"], Json["object"], video["object"],
            image["size"], javascript["size"], css["size"], flash["size"], xml["size"],
            html["size"], Json["size"], video["size"],
            image["loadTime"], javascript["loadTime"], css["loadTime"], flash["loadTime"],
            xml["loadTime"],
            html["loadTime"], Json["loadTime"], video["loadTime"],
            image["n_object"], javascript["n_object"], css["n_object"], flash["n_object"],
            xml["n_object"],
            html["n_object"], Json["n_object"], video["n_object"],
            image["n_size"], javascript["n_size"], css["n_size"], flash["n_size"], xml["n_size"],
            html["n_size"], Json["n_size"], video["n_size"],
            image["n_loadTime"], javascript["n_loadTime"], css["n_loadTime"],
            flash["n_loadTime"], xml["n_loadTime"],
            html["n_loadTime"], Json["n_loadTime"], video["n_loadTime"], total["loadTime"], total["size"],
            total["request"], non_origin_total["loadTime"], non_origin_total["size"], non_origin_total["object"],
            len(host), other["n_object"], other["n_size"], other["object"]]

        if host[0] not in site:
            site[host[0]] = []
        site[host[0]].append(row_values)

for key, value in site.items():
    median_parameter = []
    for i in range(0, len(row_values)):
        median = []
        for j in range(0, len(value)):
            median.append(value[j][i])
        #median_parameter.append(statistics.median(median))
        median.sort()
        median_parameter.append(median[int(0.9*len(median))])
    site[key] = median_parameter

with open("sitespeed.csv") as tsvfile:
    csvreader = csv.reader(tsvfile)  # , delimiter="\t"
    for line in csvreader:
        if site.get(line[0], 0) == 0:
            continue
        site[line[0]][3] = line[1]  # flash object number
        site[line[0]][19] = line[2]  # flash load time
        site[line[0]][11] = line[3]  # flash size
        site[line[0]][0] = line[4]  # ImagenumObjects
        site[line[0]][16] = line[5]  # Image loadtime
        site[line[0]][8] = line[6]  # Image byte
        site[line[0]][2] = line[7]  # css obj
        site[line[0]][18] = line[8]  # css loadtime
        site[line[0]][10] = line[9]  # css byte
        site[line[0]][1] = line[10]  # javascript obj
        site[line[0]][17] = line[11]  # javascript  load time
        site[line[0]][9] = line[12]  # javascript byte
        site[line[0]][4] = line[13]  # xml obj
        site[line[0]][20] = line[14]  # xml loadtime
        site[line[0]][12] = line[15]  # xml byte
        site[line[0]][5] = line[16]  # html obj
        site[line[0]][21] = line[17]  # html loadtime
        site[line[0]][13] = line[18]  # html byte
        site[line[0]][6] = line[19]  # json obj
        site[line[0]][22] = line[20]  # json loadtime
        site[line[0]][14] = line[21]  # json byte
        site[line[0]][7] = line[22]  # video obj
        site[line[0]][23] = line[23]  # video loadtime
        site[line[0]][15] = line[24]  # video byte

for key in site:
    row = []
    row.append(key)
    row.append(find_rank_range(rank_dict[key]))
    row.append(categories["http://www." + key])
    row = row + site[key]
    with open("90th_data.csv", 'a', newline='') as f:
        writer = csv.writer(f, dialect='excel')  # , delimiter="\t"
        writer.writerow(row)
print(image_type)
print(len(rank_spread["1-400"]), rank_spread["1-400"])
print(len(rank_spread["400-1000"]), rank_spread["400-1000"])
print(len(rank_spread["1000-2500"]), rank_spread["1000-2500"])
print(len(rank_spread["5000-10000"]), rank_spread["5000-10000"])
print(len(rank_spread["10000-20000"]), rank_spread["10000-20000"])
