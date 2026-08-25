import urllib.request
import re

url = 'https://docs.google.com/spreadsheets/d/1I74tC5idHkCxTxYUkMdM2SkaiySwvbjmljKUgctmnWE/edit'
html = urllib.request.urlopen(url).read().decode('utf-8')
tabs = re.findall(r'"name":"(.*?)"', html)
print(list(set(tabs)))
