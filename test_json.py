import json
import re
from pprint import pprint

with open('cnn_test.har', 'rb') as f:
    data =json.loads(f.read().decode("utf-8-sig"))

requestCount = 0
cssCount = 0
imageCount = 0
flashCount = 0
jsCount = 0

pattern_image = re.compile('image.*')
pattern_css=re.compile("text/css.*")
pattern_javascript=re.compile('text/.*javascript|application/.*javascript')
pattern_response=re.compile("2.*")

print(pattern_javascript.match("text/javascript"))

requestCount=len(data['log']['entries'])

for entry in data['log']['entries']:

    if(pattern_image.match(entry['response']['content']['mimeType'])and pattern_response.match(str(entry['response']['status']))):
        imageCount+=1

    if(pattern_css.match(entry['response']['content']['mimeType']) and pattern_response.match(str(entry['response']['status']))):
        cssCount+=1

    if (entry['response']['content']['mimeType']=='application/x-shockwave-flash' and pattern_response.match(str(entry['response']['status']))):
        flashCount+=1

    if (pattern_javascript.match(entry['response']['content']['mimeType'])  and pattern_response.match(str(entry['response']['status']))):
        jsCount+=1

print('requestCount:',requestCount)
print('Image Count:',imageCount)
print('scsCount+:',cssCount)
print('flashCount:',flashCount)
print('jsCount:',jsCount)

