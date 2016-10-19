import json
from haralyzer import HarParser

with open('cnn_test.har', 'r') as f:
    har_parser = HarParser(json.loads(f.read()))

requestCount = 0
cssCount = 0
imageCount = 0
flashCount = 0
jsCount = 0

for page in har_parser.pages:
    print(page)
    for entry in page.entries:

        if har_parser.match_headers(entry, 'request', 'Host', '.*', True):
            #if har_parser.match_status_code(entry, '2.*'):
                requestCount = requestCount+1

        if har_parser.match_headers(entry, 'response', 'Content-Type', 'text/css', True):
            if har_parser.match_status_code(entry, '2.*'):
                cssCount = cssCount+1

        if har_parser.match_headers(entry, 'response', 'Content-Type', 'image.*', True):
            if har_parser.match_status_code(entry, '2.*'):
                imageCount = imageCount+1

        if har_parser.match_headers(entry, 'response', 'Content-Type', 'application/x-shockwave-flash', True):
            if har_parser.match_status_code(entry, '2.*'):
                flashCount = flashCount+1

        if har_parser.match_headers(entry, 'response', 'Content-Type', 'text/javascript.*', True):
            if har_parser.match_status_code(entry, '2.*'):
                jsCount = jsCount+1

print("request number:   ", requestCount)
print("css number:       ", cssCount)
print("image number:     ", imageCount)
print("flash number:     ", flashCount)
print("javascript number:", jsCount)

# if har_parser.match_request_type(entry, 'GET'):
#     print('This is a GET request')