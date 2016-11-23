import numpy as np
import matplotlib.pyplot as plt
import json
import os
import re
import dns.resolver
import csv


def time_object_figure(dataset):
    max_num = 31
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
    plt.ylim(0, 50)
    ax1.set_title('RenderEnd and number of object', loc="left", fontsize=15)
    ax1.set_xlabel('Number of Objects', fontsize=18)
    ax1.set_ylabel('Load Time(s)', fontsize=18)
    plt.show()


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


# path = "/home/kartik/Documents/untitled folder/"
path = "D:/harsample/untitled folder/"
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

serverCache = {}
row_values = []
rank_spread = {"1-400": {}, "400-1000": {}, "1000-2500": {}, "5000-10000": {}, "10000-20000": {}}
NumOfServers = []
time_object = []
for file in dirs:
    if pattern_har.match(file):
        file = path + file
        with open(file, 'rb') as f:
            try:
                data = json.loads(f.read().decode("utf-8-sig"))
            except:
                continue
        print(file)

        host = []
        try:
            host.append(data['log']['entries'][0]['request']["headers"][0]['value'])
            host[0] = get_host(host[0])
            rank = rank_dict[host[0]]
        except:
            continue
        nameServers = []
        print(host[0])
        if serverCache.get(host[0], 0) == 0:
            try:
                serverCache[host[0]] = dns.resolver.query(host[0], "NS")
            except:
                continue
        # answer = dns.resolver.query(get_host(host[0]), "NS")
        print("serverCache", serverCache)
        for nameServer in serverCache[host[0]]:
            nameServers.append(str(nameServer)[:len(str(nameServer)) - 1])
        print("nameServers:", nameServers)

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
            #total["loadTime"] += entry['time']

            if (pattern_image.match(entry['response']['content']['mimeType']) and pattern_response.match(
                    str(entry['response']['status']))):
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

        if total["loadTime"] <= 0:
            continue

        print("hostName:", get_host(host[0]), "rank:", rank_dict[host[0]])
        print("Number of servers:", len(host))
        print("originServerNumber:", originServerNumber)
        print("non_origin_total:", non_origin_total)
        print("servers:", host)
        print('total:', total)
        print('image:', image)
        print('css:', css)
        print('flash:', flash)
        print('javascript:', javascript)
        print('xml:', xml)
        print('html:', html)
        print('json:', Json)
        print('video:', video)
        print(i)
        i += 1

        time_object.append([total["loadTime"], total["request"]])

time_object_figure(time_object)
