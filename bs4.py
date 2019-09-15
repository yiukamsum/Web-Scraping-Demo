import requests

url = "http://www.vtc.edu.hk/admission/tc/programme/s6/higher-diploma/"
data = requests.get(url)
data.encoding = "utf-8"
html = data.text

from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')
tables = soup.find_all('article', class_="courseList")
output = []
for t in tables:
    for i in t.find("table").find_all("tbody"):
        j = i.find_all("td")
        output.append([t.find('h2', class_="courseList_title").get_text(), j[2].get_text(), j[3].get_text(), [abc.get_text() for abc in i.find_all(class_="courseList_col-place")]])

import pandas as pd

df = pd.DataFrame(output, columns=['課程類別', '課程編號', '課程名稱', '開辦分校'])
df = df.explode('開辦分校')
# explode function require pandas version 0.25.0.
with open('output.csv', 'w') as file:
    file.write(df.to_csv())