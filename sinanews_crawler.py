import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import pandas
import re
import sqlite3
commentURL = '''http://comment5.news.sina.com.cn/page/info?version=1&
format=js&channel=gn&newsid=comos-{}&group=&compress=0&ie=utf-8&oe=utf-
8&page=1&page_size=20'''
def getCommentCounts(newsurl):
	m = re.search('doc-i(.*).shtml',newsurl)
	newsid = m.group(1)
	comments = requests.get(commentURL.format(newsid))
	jd = json.loads(comments.text.strip('var data='))
	return jd['result']['count']['total']

def getNewsDetail(newsurl):
	result = {}
	res = requests.get(newsurl)
	res.encoding = 'utf-8'
	soup = BeautifulSoup(res.text,'html.parser')
	result['title'] = soup.select('.main-title')[0].text
	result['newssource'] = soup.select('.source')[0].text.strip()
	timesource = soup.select('.date')[0].contents[0].strip()
	result['dt'] = datetime.strptime(timesource,'%Y年%m月%d日 %H:%M')
	result['article'] = ' '.join([p.text.strip() for p in soup.select('.article p')[:-1]])
	if(soup.select('.show_author')): 
		result['editor'] =  soup.select('.show_author')[0].text.strip('责任编辑：')
	else:
		result['editor'] = 'none'
	result['comments'] = getCommentCounts(newsurl)
	return result

def parseListLinks(url):
	newsdetails = []
	res = requests.get(url)
	res.encoding = 'utf-8'
	jd = json.loads(res.text.lstrip('  newsloadercallback(').rstrip(');'))
	for ent in jd['result']['data']:
		newsdetails.append(getNewsDetail(ent['url']))
	return  newsdetails

news_total = []
url = '''http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=gnxw&cat_2==gdxw1
||=gatxw||=zs-pl||=mtjj&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json
&page={}&callback=newsloadercallback&_=1506773283792'''
for i in range(2):
	newsurl = url.format(i)
	newsary = parseListLinks(newsurl)
	news_total.extend(newsary)	
df = pandas.DataFrame(news_total)
df.to_excel(r'C:\Users\Lenovo\Desktop\王杭宇\news.xlsx')
with sqlite3.connect('news.sqlite') as db:
	df.to_sql('news',con = db)

