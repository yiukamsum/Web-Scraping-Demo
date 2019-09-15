import requests

url = "http://www.vtc.edu.hk/admission/tc/programme/s6/higher-diploma/"
data = requests.get(url)
data.encoding = "utf-8"
html = data.text

from lxml import etree

root = etree.HTML(html)
tables = root.xpath('//article[@class="courseList"]')
output = []
for t in tables:
    for i in t.xpath('table/tbody'):
        output.append([
            t.xpath('div//h2[@class="courseList_title"]//text()')[0],
            i.xpath('tr/td[@class="courseList_col-refno"]//text()')[0],
            i.xpath('tr/td[@class="courseList_col-name"]//text()')[0],
            i.xpath('tr/td[@class="courseList_col-place"]//text()')
        ])


import pandas as pd

df = pd.DataFrame(output, columns=['課程類別', '課程編號', '課程名稱', '開辦分校'])
df = df.explode('開辦分校')
# explode function require pandas version 0.25.0.
with open('output.csv', 'w') as file:
    file.write(df.to_csv())