from bs4 import BeautifulSoup
from lxml import etree 
import urllib.request
import pandas as pd
import re

title=[]
singer=[]
#지니 차트 크롤링
def genisCrawling(page):
    url = "https://www.genie.co.kr/chart/top200?ditc=D&ymd=20240120&hh=16&rtm=Y&pg="+str(page)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Accept": "text/html"}

    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req)

    data = html.read()
    data =  data.decode("utf-8") 

    bs = BeautifulSoup(data, features="lxml")
    dom=etree.HTML(str(bs))

    
    for i in range(1,51):
        title.append(re.sub(r'\s+','',dom.xpath("/html/body/div[3]/div[2]/div[1]/div[6]/div/table/tbody/tr["+str(i)+"]/td[5]/a[1]")[0].text))
        singer.append(dom.xpath("/html/body/div[3]/div[2]/div[1]/div[6]/div/table/tbody/tr["+str(i)+"]/td[5]/a[2]")[0].text)
        #detailLink.append(dom.xpath("/html/body/div/div[3]/div/div/div[3]/form/div/table/tbody/tr["+str(i)+"]/@data-song-no"))
    #크롤링 결과 데이터 프레임에 적용

#1~200 
for i in range(1,5):
    genisCrawling(i)

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
json_file_path = './result/'+formatted_datetime+'/genisChart.json'
df.to_json(json_file_path, orient='records', lines=True,force_ascii=False)

# print(formatted_datetime)
# print(df)