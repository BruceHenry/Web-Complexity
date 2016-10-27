import json
import os
import re
import dns.resolver


def get_host(url):
    pattern_dns = re.compile('co|edu|com')
    s = url.split('.')
    if pattern_dns.match(s[len(s) - 2]):
        s = s[len(s) - 3] + '.' + s[len(s) - 2] + '.' + s[len(s) - 1]
    else:
        s = s[len(s) - 2] + '.' + s[len(s) - 1]
    return s

dirs = os.listdir("D://")
pattern_har = re.compile(".*har")

for file in dirs:
    if pattern_har.match(file):
        with open(file, 'rb') as f:
            data = json.loads(f.read().decode("utf-8-sig"))

        host = []
        host.append(data['log']['entries'][0]['request']["headers"][0]['value'])
        nameServers = []
        answer = dns.resolver.query(get_host(host[0]), "NS")
        for nameServer in answer:
            nameServers.append(str(nameServer)[:len(str(nameServer)) - 1])
        print(nameServers)

        total = {"request": 0, "size": 0, "loadTime": 0}
        css = {"object": 0, "size": 0, "loadTime": 0}
        image = {"object": 0, "size": 0, "loadTime": 0}
        flash = {"object": 0, "size": 0, "loadTime": 0}
        javascript = {"object": 0, "size": 0, "loadTime": 0}
        xml = {"object": 0, "size": 0, "loadTime": 0}
        html = {"object": 0, "size": 0, "loadTime": 0}
        Json = {"object": 0, "size": 0, "loadTime": 0}
        video = {"object": 0, "size": 0, "loadTime": 0}
        originNumber = 1
        non_origin = {"object": 0, "size": 0, "loadTime": 0}

        pattern_image = re.compile('image.*')
        pattern_css = re.compile("text/css.*")
        pattern_javascript = re.compile('text/.*javascript|application/.*script')
        pattern_xml = re.compile('test/xml.*|application/xml.*')
        pattern_html = re.compile('text/html.*')
        pattern_json = re.compile('application/json.*|text/.*json')
        pattern_video = re.compile('video.*')
        pattern_response = re.compile("2.*")

        total["request"] = len(data['log']['entries'])

        for entry in data['log']['entries']:

            total["size"] += entry['response']['content']['size']
            total["loadTime"] += entry['time']

            if (pattern_image.match(entry['response']['content']['mimeType']) and pattern_response.match(
                    str(entry['response']['status']))):
                image["object"] += 1
                image["size"] += entry['response']['content']['size']
                image["loadTime"] += entry['time']

            if (pattern_css.match(entry['response']['content']['mimeType']) and pattern_response.match(
                    str(entry['response']['status']))):
                css["object"] += 1
                css["size"] += entry['response']['content']['size']
                css["loadTime"] += entry['time']

            if (entry['response']['content']['mimeType'] == 'application/x-shockwave-flash' and pattern_response.match(
                    str(entry['response']['status']))):
                flash["object"] += 1
                flash["size"] += entry['response']['content']['size']
                flash["loadTime"] += entry['time']

            if (pattern_javascript.match(entry['response']['content']['mimeType']) and pattern_response.match(
                    str(entry['response']['status']))):
                javascript["object"] += 1
                javascript["size"] += entry['response']['content']['size']
                javascript["loadTime"] += entry['time']

            if (pattern_xml.match(entry['response']['content']['mimeType']) and pattern_response.match(
                    str(entry['response']['status']))):
                xml["object"] += 1
                xml["size"] += entry['response']['content']['size']
                xml["loadTime"] += entry['time']

            if (pattern_html.match(entry['response']['content']['mimeType']) and pattern_response.match(
                    str(entry['response']['status']))):
                html["object"] += 1
                html["size"] += entry['response']['content']['size']
                html["loadTime"] += entry['time']

            if (pattern_json.match(entry['response']['content']['mimeType']) and pattern_response.match(
                    str(entry['response']['status']))):
                Json["object"] += 1
                Json["size"] += entry['response']['content']['size']
                Json["loadTime"] += entry['time']

            if (pattern_video.match(entry['response']['content']['mimeType']) and pattern_response.match(
                    str(entry['response']['status']))):
                video["object"] += 1
                video["size"] += entry['response']['content']['size']
                video["loadTime"] += entry['time']

            find_flag = 0
            if entry['request']["headers"][0]['value'] not in host:
                host.append(entry['request']["headers"][0]['value'])
                answer = dns.resolver.query(get_host(host[len(host) - 1]), "NS")
                for ns in answer:
                    if str(ns) in nameServers:
                        originNumber += 1
                        find_flag = 1
                        break
                if find_flag == 0:
                    non_origin["object"] += 1
                    non_origin["size"] += entry['response']['content']['size']
                    non_origin["loadTime"] += entry['time']

        print("hostName:", get_host(host[0]))
        print("Number of servers:", len(host))
        print("originNumber:", originNumber)
        print("non_origin:", non_origin)
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
        print()
