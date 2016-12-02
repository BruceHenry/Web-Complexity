import json
import os
import re
import dns.resolver
#from sets import Set
import shelve
import hashlib


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

rankmap = {}
with open('ranklist','r') as f:
    for line in f.read().splitlines():
        rankmap[line.split('\t')[1]] = int(line.split('\t')[0])



def checksum_md5(filename, blocksize=2**20):
    m = hashlib.md5()
    with open( filename , "rb" ) as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update( buf )
    return m.hexdigest()

# path = "../networkingresearch/sitespeed-result/"
# harfiles = os.listdir(path)

dns_queries = shelve.open('dnsqueries.dat', protocol=-1)
files_opened = shelve.open('filesopened.dat', protocol=-1, writeback=True)
if 'files' not in files_opened:
    files_opened['files'] = []
site_stats = {}

resolver = dns.resolver.Resolver()
resolver.timeout = 4
resolver.lifetime = 4

harfiles = []

for root, dirs, files in os.walk("""/Users/enadel/Onedrive/Documents/CS 513/"""):
    for file in files:
        if file.endswith(".har"):
            harfiles.append(os.path.join(root, file))


for file in harfiles:

    if checksum_md5(file) in files_opened['files']:
        print "analyzed already..."
        continue


    with open(file, 'rb') as f:
        try:
            data = json.loads(f.read().decode("utf-8-sig"))
        except:
            continue

    #print(file)
    host = []
    try:
        host.append(data['log']['entries'][0]['request']["headers"][0]['value'])
    except:
        continue

    nameServers = []
    if dns_queries.has_key(str(get_host(host[0]))):
        answer = dns_queries[str(get_host(host[0]))]
    else:
        try:
            answer = resolver.query(get_host(host[0]), "NS")
        except Exception as e:
            continue
        dns_queries[str(get_host(host[0]))] = answer

    for nameServer in answer:
        nameServers.append(str(nameServer)[:len(str(nameServer)) - 1])


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
    total["loadTime"] = data['log']['pages'][0]['pageTimings']['onLoad']
    for entry in data['log']['entries']:

        total["size"] += entry['response']['content']['size']
        total["loadTime"] = data['log']['pages'][0]['pageTimings']['onLoad']


        if 'mimeType' in entry['response']['content']:
            if entry['time'] is None:
                entry['time'] = 0
            if entry['response']['content']['size'] < 0:
                entry['response']['content']['size'] = entry['response']['bodySize']
                if entry['response']['content']['size'] < 0:
                    if 'headersSize' not in entry['response']:
                        continue
                    else:
                        entry['response']['content']['size'] = entry['response']['headersSize']

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

        try:
            if entry['request']["headers"][0]['value'] not in host:
                host.append(entry['request']["headers"][0]['value'])
                answer = resolver.query(get_host(host[len(host) - 1]), "NS")
                for ns in answer:
                    if str(ns)[:len(str(ns)) - 1] in nameServers:
                        originNumber += 1
                        find_flag = 1
                        break
                if find_flag == 0:
                    non_origin["object"] += 1
                    non_origin["size"] += entry['response']['content']['size']
                    non_origin["loadTime"] += entry['time']
        except:
            pass


    hostname = str(host[0].replace('www.','').replace('ww1.',''))

    if hostname in rankmap:

        site_stats = shelve.open('sitedataparsed/'+ hostname + '.dat', protocol=-1, writeback=True)

        if hostname not in site_stats:
            site_stats[hostname] = {'hostName': hostname,
                                'rank': rankmap[hostname],
                                'numberofservers': len(host),
                                'originnumber': originNumber,
                                'nonorigin': non_origin,
                                'servers': Set(host),
                                'total': total,
                                'image': image,
                                'css': css,
                                'flash': flash,
                                'javascript': javascript,
                                'xml': xml,
                                'html': html,
                                'json': Json,
                                'video': video,
                                'numrecords': 1}
        else:
            site_stats[hostname]['numberofservers'] = max(site_stats[hostname]['numberofservers'],len(host))
            site_stats[hostname]['originnumber'] += max(site_stats[hostname]['originnumber'],originNumber)

            site_stats[hostname]['nonorigin']['object'] += non_origin['object']
            site_stats[hostname]['nonorigin']['size'] += non_origin['size']
            site_stats[hostname]['nonorigin']['loadTime'] += non_origin['loadTime']

            site_stats[hostname]['servers'].update(Set(host))

            site_stats[hostname]['total']['loadTime'] += total['loadTime']
            site_stats[hostname]['total']['request'] += total['request']
            site_stats[hostname]['total']['size'] += total['size']

            site_stats[hostname]['image']['object'] += image['object']
            site_stats[hostname]['image']['size'] += image['size']
            site_stats[hostname]['image']['loadTime'] += image['loadTime']

            site_stats[hostname]['css']['object'] += css['object']
            site_stats[hostname]['css']['size'] += css['size']
            site_stats[hostname]['css']['loadTime'] += css['loadTime']

            site_stats[hostname]['flash']['object'] += flash['object']
            site_stats[hostname]['flash']['size'] += flash['size']
            site_stats[hostname]['flash']['loadTime'] += flash['loadTime']

            site_stats[hostname]['javascript']['object'] += javascript['object']
            site_stats[hostname]['javascript']['size'] += javascript['size']
            site_stats[hostname]['javascript']['loadTime'] += javascript['loadTime']

            site_stats[hostname]['xml']['object'] += xml['object']
            site_stats[hostname]['xml']['size'] += xml['size']
            site_stats[hostname]['xml']['loadTime'] += xml['loadTime']

            site_stats[hostname]['html']['object'] += html['object']
            site_stats[hostname]['html']['size'] += html['size']
            site_stats[hostname]['html']['loadTime'] += html['loadTime']

            site_stats[hostname]['json']['object'] += Json['object']
            site_stats[hostname]['json']['size'] += Json['size']
            site_stats[hostname]['json']['loadTime'] += Json['loadTime']

            site_stats[hostname]['video']['object'] += video['object']
            site_stats[hostname]['video']['size'] += video['size']
            site_stats[hostname]['video']['loadTime'] += video['loadTime']

            site_stats[hostname]['numrecords'] += 1

        print "Hostname: " + hostname + " numRecords: " + str(site_stats[hostname]['numrecords'])
        site_stats.close()

    files_opened['files'].append(checksum_md5(file))



for file in os.listdir('sitedataparsed/'):

    site_stats = shelve.open('sitedataparsed/' + file, protocol=-1)
    hostn = site_stats.keys()[0]

    print (site_stats[hostn]['total']['request'] / site_stats[hostn]['numrecords'])

    #first write column headers
    csvWriter.writerow(list(mydict.keys())

    #now data, assuming each column has the same # of values
    for i in xrange(len(mydict['Date'])):
        csvWriter.writerow([mydict[k][i] for k in mydict.keys()])
