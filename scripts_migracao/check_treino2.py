import urllib.request
import re
import urllib.parse
import pandas as pd

url = 'https://docs.google.com/spreadsheets/d/1I74tC5idHkCxTxYUkMdM2SkaiySwvbjmljKUgctmnWE/htmlview'
html = urllib.request.urlopen(url).read().decode('utf-8')
# The htmlview has a list of sheets in a javascript object or html.
# Let's just find "Treino_phyton" in the html
if "Treino_phyton" in html:
    print("YES, Treino_phyton is in HTML")
else:
    print("NO, Treino_phyton not in HTML")

# Try to download using gviz
url2 = f"https://docs.google.com/spreadsheets/d/1I74tC5idHkCxTxYUkMdM2SkaiySwvbjmljKUgctmnWE/gviz/tq?tqx=out:csv&sheet={urllib.parse.quote('Treino_phyton')}"
try:
    df = pd.read_csv(url2)
    print("Columns:", df.columns.tolist())
    print(df.head())
except Exception as e:
    print(e)
