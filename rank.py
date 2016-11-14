
import requests


categorymap = {}
rankmap = {}
# with open('random_2000_gold.txt','r') as f:
#     for line in f.read().splitlines():
#         rankmap[line.split('\t')[1]] = int(line.split('\t')[0])
#         r = requests.post('https://wrapapi.com/use/kireledan/networking/siteinfo/latest',
#             data = {'wrapAPIKey':'NiyzR6d6hxcI7JUbTXdP9A9aG1KwlOSP', 'URL':line.split('\t')[1]})
#         print r.text[7:r.text.find('>')-1]
#         categorymap[line.split('\t')[1]] = r.text[7:r.text.find('>')-1]



print categorymap
with open('categories', 'w') as f:
    f.write(str(rankmap))


array = [19, 13, 13, 19, 19, 11, 16, 11, 13, 13, 13, 31, 13, 19, 8, 18, 17, 13, 8, 11, 13, 19, 19, 16, 8, 16, 13, 17, 8, 19, 8, 15, 13, 8, 19, 13, 19, 8, 11, 11, 11, 8, 19, 11, 13, 13, 17, 8, 11, 19, 13, 8, 11, 8, 10, 13, 8, 11, 19, 13, 8, 13, 10, 17, 13, 11, 8, 19, 8, 13, 16, 11, 19, 19, 8, 10, 13, 13, 8, 11]

array.sort()
print array

def percentage(num, array):
    numSmallerorEq = 0
    for item in array:
        if item <= num:
            numSmallerorEq += 1
    return float(numSmallerorEq) / float(len(array))

for item in array:
    print str(item) + ", " + str(percentage(item, array))
