import json

import re

from pprint import pprint

with open('cnn_test.har', 'rb') as f:
    data = json.loads(f.read().decode("utf-8-sig"))

distinctServer = 0
host = []

requestCount = 0

cssCount = 0
imageCount = 0
flashCount = 0
jsCount = 0
xmlCount = 0
htmlCount = 0
jsonCount = 0
videoCount = 0

totalSize = 0
cssSize = 0
imageSize = 0
flashSize = 0
jsSize = 0
xmlSize = 0
htmlSize = 0
jsonSize = 0
videoSize = 0

totalTime = 0
cssTime = 0
imageTime = 0
flashTime = 0
jsTime = 0
xmlTime = 0
htmlTime = 0
jsonTime = 0
videoTime = 0

pattern_image = re.compile('image.*')
pattern_css = re.compile("text/css.*")
pattern_javascript = re.compile('text/.*javascript|application/.*script')
pattern_xml = re.compile('test/xml.*|application/xml.*')
pattern_html = re.compile('text/html.*')
pattern_json = re.compile('application/json.*|text/.*json')
pattern_video = re.compile('video.*')
pattern_response = re.compile("2.*")

requestCount = len(data['log']['entries'])

for entry in data['log']['entries']:

    totalSize += entry['response']['content']['size']
    totalTime += entry['time']

    if (pattern_image.match(entry['response']['content']['mimeType']) and pattern_response.match(
            str(entry['response']['status']))):
        imageCount += 1
        imageSize += entry['response']['content']['size']
        imageTime += entry['time']

    if (pattern_css.match(entry['response']['content']['mimeType']) and pattern_response.match(
            str(entry['response']['status']))):
        cssCount += 1
        cssSize += entry['response']['content']['size']
        cssTime += entry['time']

    if (entry['response']['content']['mimeType'] == 'application/x-shockwave-flash' and pattern_response.match(
            str(entry['response']['status']))):
        flashCount += 1
        flashSize += entry['response']['content']['size']
        flashTime += entry['time']

    if (pattern_javascript.match(entry['response']['content']['mimeType']) and pattern_response.match(
            str(entry['response']['status']))):
        jsCount += 1
        jsSize += entry['response']['content']['size']
        jsTime += entry['time']

    if (pattern_xml.match(entry['response']['content']['mimeType']) and pattern_response.match(
            str(entry['response']['status']))):
        xmlCount += 1
        xmlSize += entry['response']['content']['size']
        xmlTime += entry['time']

    if (pattern_html.match(entry['response']['content']['mimeType']) and pattern_response.match(
            str(entry['response']['status']))):
        htmlCount += 1
        htmlSize += entry['response']['content']['size']
        htmlTime += entry['time']

    if (pattern_json.match(entry['response']['content']['mimeType']) and pattern_response.match(
            str(entry['response']['status']))):
        jsonCount += 1
        jsonSize += entry['response']['content']['size']
        jsonTime += entry['time']

    if (pattern_video.match(entry['response']['content']['mimeType']) and pattern_response.match(
            str(entry['response']['status']))):
        videoCount += 1
        videoSize += entry['response']['content']['size']
        videoTime += entry['time']

    if (entry['request']["headers"][0]['value'] not in host):
        host.append(entry['request']["headers"][0]['value'])

s = host[0]
hostName = ""
n = 1
count = 0
while count != 2:
    c = s[len(s) - n]
    hostName = c + hostName
    if c != '.':
        n += 1
        continue
    count += 1
    n += 1
hostName = hostName[1:len(hostName)]

print("hostName:", hostName)
print(host)
print('requestCount:', requestCount)
print('total size,time:', totalSize, totalTime)
print('Image Count,size,time:', imageCount, imageSize, imageTime)
print('css Count,size,time:', cssCount, cssSize, cssTime)
print('flash Count,size,time:', flashCount, flashSize, flashTime)
print('js Count,size,time:', jsCount, jsSize, jsTime)
print('xml Count,size,time:', xmlCount, xmlSize, xmlTime)
print('html Count,size,time:', htmlCount, htmlSize, htmlTime)
print('json Count,size,time:', jsonCount, jsonSize, jsonTime)
print('video Count,size,time:', videoCount, videoSize, videoTime)
