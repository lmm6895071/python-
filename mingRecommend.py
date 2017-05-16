# coding:utf-8
import requests
import sys
import re
import json
import base64
import time,datetime
import threading
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding("utf8")

def urls():
    urls=["Stop-Shoulder-Pains","Care-for-the-Elderly","cure a fever at home","treat a sprained ankle","care for a baby","care for a pet"]
    for index in urls:
        url ="http://www.wikihow.com/"+index
        mingTest(url)
        print "----------------------------------------------------------------------------------------------S"
def mingTest(url):
    print url
    try:
        responses = requests.get(url,timeout=2)
    except:
        print "failed"
        return
    result = responses.text
    html = BeautifulSoup(result,"lxml")
    results=[]
    print "标题:\n"
    for item in html.find_all("h1",attrs={"class" : "firstHeading"}):
        for t in  item.find_all("a"):
             pattern=r"<a.*?>(.*?)</a>"
             cc=re.findall(pattern,str(t),re.I)
             for c in cc:
	         temp=c.decode('utf-8')
             results.append(temp)
             print temp

    contents=[]
    print "内容:"
    s=html.select("#intro p")
    for i in s:
        print i.text.encode("utf-8")
    ls=html.find_all("div",attrs={"class": "section steps   sticky "})
    for item in ls:
        pattern=r"<span.*?>(.*?)</span>"
        cc=re.findall(pattern,str(item),re.I)
        contents.append(cc.encode("utf-8"))
        print cc
    ls=html.find_all("div",attrs={"class":"step"})
    for item in ls:
        contents.append(item.text.encode("utf-8"))
        print item.text.encode("utf-8")
    
if __name__ == "__main__":
    urls()
    url ="http://www.wikihow.com/Keep-Your-Kitchen-Clean-and-Safe"
    mingTest(url)