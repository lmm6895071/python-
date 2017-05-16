# encoding: utf-8

import requests
import json
import base64
import re
import threading
from traceback import format_exc
from lxml import etree
import sys
import logging
reload(sys)

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                  datefmt='%a, %d %b %Y %H:%M:%S')
sys.setdefaultencoding('utf8')
def getsBaiduHotWord(): 
    data=[]
    url='http://top.baidu.com/buzz/top10.html'
    try:
        response=requests.get(url=url)
    except Exception as err:
        logging.error("hotWord baidu url failed;"+str(err))
        return None  
    tree = etree.HTML(response.text.encode(response.encoding))
    mod_relation=tree.xpath('/html/body/div[@class="wrapper"]/div[@class="main"]/div[@class="mainBody"]/div[@class="grayborder"]/table[@class="list-table"]')
    if mod_relation is not None and len(mod_relation)>0:
        allth=mod_relation[0].xpath('.//tr')
        for th in allth:
            try:
                a=th.xpath('./td[@class="keyword"]//a')
                if len(a)<=0:
                	continue
                title=a[0].xpath('string(.)').strip()
                if title not in data:
                   data.append(title)
            except Exception as err:
                logging.error(" hotWord parse baidu content error;"+str(err)) 
    mutex.acquire()
    datas["百度热搜榜"]=data
    mutex.release()  

def getNew360Hotword():
    data=[]
    url='http://sh.qihoo.com/api/hot_new.json?jsonp=1&callback=HotAjax.loadOk&type=day0&t=830469'
    try:
        response=requests.get(url=url)
    except Exception as err:
        logging.error("hotWord s360 url failed;"+str(err))
        return None  
    result=(response.text)
    pattern = r"\"keyword\":(.*?),"
    results=re.findall(pattern,result,re.I)
    print len(results)
    try:
        for item in results:
            dt = eval("u"+item)
            if dt not in data:
                data.append(dt)
    except Exception as err:
    	logging.error(" hotWord parse new360 content error;"+str(err)) 
    mutex.acquire()
    datas["新360热搜榜"]=data
    mutex.release()  
def gets360HotWord(): 
    data=[]
    url='http://top.so.com/hotnews/detail'
    try:
        response=requests.get(url=url)
    except Exception as err:
        logging.error("hotWord s360 url failed;"+str(err))
        return None  
    tree = etree.HTML(response.text)
    mod_relation=tree.xpath('/html/body/div[@id="wrapper"]/div[contains(@class,"content")]/div[@class="main-wrapper"]/table[@class="ranklist"]')
    if mod_relation is not None and len(mod_relation)>0:
        rs=mod_relation[0].xpath('./tbody')
        if rs is not None and len(rs)>0:
            allth=rs[0].xpath('./tr')
            for th in allth:
                try:
                    a=th.xpath('./td[@class="rankitem__info"]//a')
                    title=a[0].xpath('string(.)').strip()
                    if title not in data:
                       data.append(title)
                except Exception as err:
                    logging.error(" hotWord parse s360 content error;"+str(err)) 
    mutex.acquire()
    datas["360热搜榜"]=data
    mutex.release()  
def getSogouHotWord():
    data=[]
    for index in range(3):
        url='http://top.sogou.com/hot/shishi_'+str(index+1)+'.html'
        try:
            response=requests.get(url=url)
        except Exception as err:
            logging.error("hotWord sogou url failed;"+str(err))
            return None
        tree = etree.HTML(response.text.encode(response.encoding))
        hintBox=tree.xpath('/html/body/div[@class="contant"]/div[@class="main"]/ul[@class="pub-list"]')
        if hintBox is not None and len(hintBox)>0:
            alltd=hintBox[0].xpath('./li')
            for td in alltd:
                try:
                    a=td.xpath('./span[@class="s2"]/p[@class="p1"]/a | ./span[@class="s2"]/p[@class="p3"]/a')
                    title=a[0].xpath('string(.)').strip()
                    if title not in data:
                       data.append(title)
                except Exception as err:
                    logging.error("hotWord parse sogou content error;"+str(err)) 
    mutex.acquire()
    datas["搜狗热搜榜"]=data
    mutex.release()  

def getChinaSOHotWord():
	data=[]
	url="http://www.chinaso.com/search/api/hotsug.json?callback=jQuery19104863119341724025_1487744241984&_=1487744241985"          
	try:
		response=requests.get(url,timeout=5)
	except Exception as err:
		logging.error("hotWord sogou url failed;"+str(err))
		return None
	html=response.text
	pattern=r'fullTitle\":\"(.*?)\"'
	result=re.findall(pattern,html,re.I)

	for item in result:
		if item =="" or item ==" " or item =="\n":
			continue
		data.append(item)
	mutex.acquire()
	datas["国搜热搜榜"]=data
	mutex.release()

def start():
    global datas, mutex
    mutex = threading.Lock()
    threads = []
    datas={}
    threads.append(threading.Thread(target=getNew360Hotword))
    threads.append(threading.Thread(target=getSogouHotWord))
    threads.append(threading.Thread(target=gets360HotWord))
    threads.append(threading.Thread(target=getsBaiduHotWord))
    threads.append(threading.Thread(target=getChinaSOHotWord))
    threads.append(threading.Thread(target=getsBaiduHotWord))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    if '' in datas:
        datas.pop("",None)
    return datas  
                                       
if __name__ == "__main__":
    mydata=start()
    mydata = json.dumps(mydata, ensure_ascii=False)
    print mydata
