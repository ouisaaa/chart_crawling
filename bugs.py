from bs4 import BeautifulSoup
from lxml import etree 
import urllib.request
import pandas as pd
import re

#벅스 차트 크롤링
url = "https://music.bugs.co.kr/chart"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Accept": "text/html"}

req = urllib.request.Request(url, headers=headers)
html = urllib.request.urlopen(req)

data = html.read()
data =  data.decode("utf-8") 

bs = BeautifulSoup(data, features="lxml")
dom=etree.HTML(str(bs))

title=[]
singer=[]

# csv_title=dom.xpath("/html/body/div[2]/div[2]/article/section/div/fieldset/time")[0].text+"."+dom.xpath("/html/body/div[2]/div[2]/article/section/div/fieldset/time/em")[0].text

# csv_title_result=re.sub(r'\s','',csv_title)

for i in range(1,101):
    title.append(dom.xpath("/html/body/div[2]/div[2]/article/section/div/div[1]/table/tbody/tr["+str(i)+"]/th/p/a")[0].text)
    singer.append(dom.xpath("/html/body/div[2]/div[2]/article/section/div/div[1]/table/tbody/tr["+str(i)+"]/td[5]/p/a")[0].text)
    #detailLink.append(dom.xpath("/html/body/div/div[3]/div/div/div[3]/form/div/table/tbody/tr["+str(i)+"]/@data-song-no"))
#크롤링 결과 데이터 프레임에 적용
titles=pd.Series(title)
singers=pd.Series(singer)
#links=pd.Series(detailLink)

df=pd.DataFrame({
    'title':titles,
    'singer':singers,
    #'detailLink':links
})

from datetime import datetime

current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:00:00")

# 데이터프레임을 JSON 파일로 저장
json_file_path = './result/'+formatted_datetime+'/bugsChart.json'
df.to_json(json_file_path, orient='records', lines=True,force_ascii=False)

# print(csv_title_result)
# print(df)