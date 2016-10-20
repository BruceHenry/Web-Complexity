import json

import re

from pprint import pprint

with open('google.har', 'rb') as f:
    data = json.loads(f.read().decode("utf-8-sig"))

requestCount = 0
cssCount = 0
imageCount = 0
flashCount = 0
jsCount = 0
xmlCount = 0
htmlCount = 0
jsonCount = 0
videoCount = 0

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
    if (pattern_image.match(entry['response']['content']['mimeType']) and pattern_response.match(
            str(entry['response']['status']))):
        imageCount += 1
    if (pattern_css.match(entry['response']['content']['mimeType']) and pattern_response.match(
            str(entry['response']['status']))):
        cssCount += 1
    if (entry['response']['content']['mimeType'] == 'application/x-shockwave-flash' and pattern_response.match(
            str(entry['response']['status']))):
        flashCount += 1
    if (pattern_javascript.match(entry['response']['content']['mimeType']) and pattern_response.match(
            str(entry['response']['status']))):
        jsCount += 1
    if (pattern_xml.match(entry['response']['content']['mimeType']) and pattern_response.match(
            str(entry['response']['status']))):
        xmlCount += 1
    if (pattern_html.match(entry['response']['content']['mimeType']) and pattern_response.match(
            str(entry['response']['status']))):
        htmlCount += 1
    if (pattern_json.match(entry['response']['content']['mimeType']) and pattern_response.match(
            str(entry['response']['status']))):
        jsonCount += 1
    if (pattern_video.match(entry['response']['content']['mimeType']) and pattern_response.match(
            str(entry['response']['status']))):
        videoCount += 1

print('requestCount:', requestCount)
print('Image Count:', imageCount)
print('cssCount:', cssCount)
print('flashCount:', flashCount)
print('jsCount:', jsCount)
print('xmlCount:', xmlCount)
print('htmlCount:', htmlCount)
print('jsonCount:', jsonCount)
print('videoCount:', videoCount)
