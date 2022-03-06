import requests 
from bs4 import BeautifulSoup
import time


# =================================Scraping====================================

def extractDetails(URL,storedBlock):
    r = requests.get(URL).text
    soup = BeautifulSoup(r, 'lxml')
    table=soup.find('div',class_='hnfgic-0 enzKJw')
    hashcode,timeStamp,block='','',''
    for i in table.findAll('div',class_='sc-1enh6xt-0 kiseLw'):
        heading,value=i.findAll('div',class_='sc-8sty72-0 bFeqhe')
        column=heading.text
        if column=='Hash':
            hashcode=value.text
        if column=='Timestamp':
            DateTime=value.text+':00+00:00'.split('+')[0]
            timeStamp=int(time.mktime(time.strptime(DateTime, '%Y-%m-%d %H:%M:%S')))
        if column=='Height':
            block=value.text
    if str(block)==str(storedBlock):
        print('Block Hit!')
        return None
    print(hashcode,block,timeStamp)
    return(hashcode,block,timeStamp)

def ScrapeBlockchain(blockNumber):
    page=1
    ScrapedAData=[]  
    loop=True
    while loop:
        URL = "https://www.blockchain.com/btc/blocks?page="+str(page)
        r = requests.get(URL).text
        soup = BeautifulSoup(r, 'lxml')
        article=soup.find('div',class_='rjh6gp-0 eJQZzB')
        count=0
        for i in article.findAll('div',class_='sc-1g6z4xm-0 hXyplo'):
            count+=1
            try:
                PostUrl=i.find('a')["href"]
                Details=extractDetails('https://www.blockchain.com'+PostUrl,blockNumber)
                if Details==None:
                    loop=False
                    break
                ScrapedAData.append(list(Details))
            except Exception as e:
                print('ScrapeBlockchain exception',e)
                continue
        page+=1
    return ScrapedAData


# ==============================Count calculation=================================

def PrepareCount(ScrapedAData,prevTimeStamp,count):
    for index,value in enumerate(ScrapedAData):
        currentTimeStamp=value[2]
        if (currentTimeStamp-prevTimeStamp)/3600 >2:
            count+=1
        ScrapedAData[index].append(count)
        prevTimeStamp=currentTimeStamp
    return ScrapedAData

# ==============================For Posting Data=================================

def postData(PreparedData):
    POST_URL = 'http://localhost:5000/postinfo'
    post_data = {"data_type": "latest_mined_blocks", "data": PreparedData}
    ret = requests.post(POST_URL, json=post_data)
    print(ret)
    return

# ==============================For Recieving Data=================================

def getData():
    GET_URL = 'http://localhost:5000/getinfo'
    ret = requests.get(GET_URL).json()
    return ret['blockNumber'],ret['count'],ret['timestamp']

# ==============================Main=================================

while True:
    print('starting scraping')
    blockNumber,count,prevTimeStamp=getData()
    ScrapedAData=ScrapeBlockchain(blockNumber)[::-1]
    print('scraping done')
    PreparedData=PrepareCount(ScrapedAData,prevTimeStamp,count)
    print('data prepared')
    postData(PreparedData)
    print('data posted')
    time.sleep(600)
