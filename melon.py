from bs4 import BeautifulSoup
from lxml import etree 
import urllib.request
import pandas as pd

#멜론 차트 크롤링
url = "https://www.melon.com/chart/index.htm"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36", "Accept": "text/html"}

req = urllib.request.Request(url, headers=headers)
html = urllib.request.urlopen(req)

data = html.read()
data =  data.decode("utf-8") 

bs = BeautifulSoup(data, features="lxml")
dom=etree.HTML(str(bs))

title=[]
singer=[]
detailLink=[]
for i in range(1,101):
    title.append(dom.xpath("/html/body/div/div[3]/div/div/div[3]/form/div/table/tbody/tr["+str(i)+"]/td[6]/div/div/div[1]/span/a")[0].text)
    singer.append(dom.xpath("/html/body/div/div[3]/div/div/div[3]/form/div/table/tbody/tr["+str(i)+"]/td[6]/div/div/div[2]/span/a")[0].text)
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
print(df)