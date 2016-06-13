# -*- coding: utf-8 -*-

import urllib
import codecs
from bs4 import BeautifulSoup 

def retriveCodeTable(content):
	soup = BeautifulSoup(content.decode("utf-8"))
	#soup = BeautifulSoup(content)
	form_stock = soup.select('form[name="stock"] a ')
	for a in form_stock:
		print a.text.strip().encode("utf-8")

proxy = {"https":"http://127.0.0.1:3128"}
proxy = {"http":"http://127.0.0.1:3128"}
stockCodeNameUrl="https://tw.stock.yahoo.com/h/kimosel.php?tse=1&cat=%A5b%BE%C9%C5%E9&form=menu&form_id=stock_id&form_name=stock_name&domain=0"
url = "http://tw.yahoo.com"
#stockCodeNameUrl = "https://tw.stock.yahoo.com"+"/h/kimosel.php?tse=1&cat=%E9%9B%BB%E6%A9%9F&form=menu&form_id=stock_id&form_name=stock_name&domain=0"
#filehandle = urllib.urlopen(stockCodeNameUrl, proxies=proxy)
#content = filehandle.read()
#print content.decode("big5").encode("utf8")
stockUrlBase = "https://tw.stock.yahoo.com"
content = open("stock.html").read()


soup = BeautifulSoup(content.decode("utf-8"))
link_stock = soup.select('tr > td > a[href]')
for lid, l in enumerate(link_stock):
	if "tse=2" in l['href'].strip():
		continue
	stockCodeNameUrl = stockUrlBase + l['href'].strip()
	filehandle = urllib.urlopen(stockCodeNameUrl, proxies = proxy)
	content = filehandle.read()
	try:
		retriveCodeTable(content.decode("big5").encode("utf8"))
	except:
		print l.text.encode("utf8"), lid
		

#to get individual codename such as 1535 中宇
#soup = BeautifulSoup(content.decode("utf-8"))
#form_stock = soup.select('form[name="stock"] a ')
#for a in form_stock:
#	print a.text.strip()
