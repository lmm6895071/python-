#-*- encoding:utf-8-*-

import os
import sys
import requests
import json


'''
fs = open("1.txt",'r')

ls= fs.read()
fs.close()

ls=ls.replace("\n"," ")
type(ls)
ls =ls.split("#")
print len(ls)
fs= open("w.txt",'w')
for tm in ls:
	tm=tm.strip(" ")
	fs.write(tm+'\n')
fs.close()
'''
def appendWord():
	url ="http://111.202.25.48:8081/iie-icm/login/login.do"

	header={'Accept':'application/json, text/javascript, */*; q=0.01',
	'Accept-Encoding':'gzip, deflate, sdch',
	'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
	'Connection':'keep-alive',
	'Cookie':'PMSESSIONID=37d3ebb9-827e-4932-94b8-d7807d304b53',
	'Host':'111.202.25.48:8081',
	'Referer':'http://111.202.25.48:8081/iie-icm/indexpage.do',
	'Upgrade-Insecure-Requests':'1',
	'Content-Type':'application/json;charset=UTF-8;',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
			 'X-Requested-With': 'XMLHttpRequest'
			}

	para={"loginId":"admin",'loginPwd':"admin"}
	session = requests.Session()
	respones= session.post(url,data=json.dumps(para),headers=header)
	#result = session.get('http://111.202.25.48:8080/live/live/addKeywords.action?id=12312268',headers=header)
	print respones.text

	url ='http://111.202.25.48:8081/iie-icm/subjectmonitor/saveEventAndKeys.do'
	url ='http://111.202.25.48:8081/iie-icm/subjectmonitor/tosubjectmonitor.do?ctype=1'

	result = session.get(url,headers=header)
	header['Referer']="http://111.202.25.48:8081/iie-icm/subjectmonitor/tosubjectmonitor.do?ctype=1"
	header['Content-Type']="application/x-www-form-urlencoded; charset=UTF-8"
	print result.text
	url='http://111.202.25.48:8081/iie-icm/subjectmonitor/queryTableFormRule.do'
	para= {'id':'12312268'}
	result = session.post(url,data=(para),headers=header)
	result= result.text
	print result
	result = json.loads(result)
	print type(result)
	datas= result['data']

	k1=datas[-1].keys()[0]
	k2=datas[-1].keys()[1]
	w=u"叛逃郭文贵"
	k1=u"关键词"
	k2=u'去除词'
	temp={k1:[w],k2:''}
	print temp[temp.keys()[1]]
	datas.append(temp)
	result['data']=datas


	result = str(result).replace("u\'","\"")
	result= str(result).replace('\'','\"')
	result=result.decode("unicode-escape")
	print type(result),result
	print "header :",header
	para1={'id':12312268,'sid':12312266,'datas':result}

	header['Cookie']="PMSESSIONID=37d3ebb9-827e-4932-94b8-d7807d304b53"
	header['Accept-Language']="zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3"


	url='http://111.202.25.48:8081/iie-icm/subjectmonitor/saveEventAndKeys.do'
	result=session.post(url,data=(para1),headers=header)
	print result,result.text

def show():
	header={
		#'POST http':'http//111.202.25.48:8080/live/reg/login.action HTTP/1.1',
	'Accept': 'application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*',
	'Referer': 'http://111.202.25.48:8080/live/reg/index.action',
	'Accept-Language': 'zh-CN',
	'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)',
	'Content-Type': 'application/x-www-form-urlencoded',
	'Accept-Encoding': 'gzip, deflate',
	'Connection': 'Keep-Alive',
	'DNT': '1',
	'Host': '111.202.25.48:8080',
	'Pragma': 'no-cache',
	'Cookie': 'JSESSIONID=FEA80E580F4FE9736F777C2E93587EBC'
	}
	para={"password":"wxb-abcd-1234",'name':"admin"}
	url='http://111.202.25.48:8080/live/reg/login.action'
	session = requests.Session()
	respones= session.post(url,data=(para),headers=header,)
	result = session.get('http://111.202.25.48:8080/live/live/addKeywords.action?id=12312268',headers=header)
	print "8080######:",result.text

#show()
appendWord()




