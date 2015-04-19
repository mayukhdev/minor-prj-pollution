#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import re
import pprint
import requests
from bs4 import BeautifulSoup
from datetime import datetime

month = {
			'January' : 1, 'February': 2 ,'March' : 3,
            'April':4, 'May':5, 'June':6,
            'July':7,'August':8,'September':9,
            'October':10,'November':11,'December':12
        }

data = {
			"place" : u"",
			"ozone" : None,
			"dateExtracted" : datetime(2015,1,1,0,0),
			"unit" : u'\u03bc' + u'g/m'+ u'\xb3',
			"particulate2.5" : None,
			"particulate10" : None
	   }

#R.K Puram
data['place'] = u"R.K Puram"
url = "http://www.dpccairdata.com/dpccairdata/display/rkPuramView15MinData.php"
while True:
	try:
		r = requests.get(url)
		break
	except:
		print "Error " + str(r.status_code)
		continue
#with open("rkp",'w') as f:
	#f.write(r.text.encode('utf-8'))
soup = BeautifulSoup(r.text)
some_elements_1 =  soup.find_all('tr',class_='tdcolor1')
some_elements_2 =  soup.find_all('tr',class_='tdcolor2')

for td in some_elements_1:
	flag_str = 0
	flag_val = 0
	date = []
	for i in td:
		nav_text = i.string
		word =  unicode(nav_text)
		if (nav_text!="Ozone" or re.search(r'Particulate',word)) and flag_str==0:
			continue
		flag_str = 1
		if nav_text =="Ozone":
			continue
		if nav_text!=None:			
			if re.search(r'\d+',word):
				if re.search(r'2015',word):
					day = word.strip().split(",")
					m , d = map(str,day[1].strip().split(" "))
					date.append(2015)
					date.append(month[m])
					date.append(int(d))
				else:
					h,mi,s =  map(int,word.strip().split(":"))
					date.append(h)
					date.append(mi)
					date.append(s)
			continue		
		for k in i:
			try:
				if flag_val==0:
					num = re.search(r"\d+.\d+",k).group()
					data['ozone'] = int(num)
					#If data not updated will save the Standard
					flag_val+=1
			except:
				continue
	if len(date)>0:
		data['dateExtracted'] = datetime(date[0],date[1],date[2],date[3],date[4],date[5])

for td in some_elements_1:
	flag_val = 0
	flag_str = 0
	for i in td:
		nav_text = i.string
		word =  unicode(nav_text)
		if re.search(r'Particulate',word):
			flag_str+=1
			continue
		if flag_str==1 and nav_text==None:
			for k in i:
				try:
						if flag_val==0 and re.search(r"\d+",k):
							num = re.search(r"\d+",k).group()
							data['particulate10'] = int(num)
							#If data not updated will save the Standard
							flag_val+=1
				except:
						continue

for td in some_elements_2:
	flag_val = 0
	flag_str = 0
	for i in td:
		nav_text = i.string
		word =  unicode(nav_text)
		if re.search(r'Particulate',word):
			flag_str+=1
			continue
		if flag_str==1 and nav_text==None:
			for k in i:
				try:
					if flag_val==0 and re.search(r"\d+",k):
						num = re.search(r"\d+",k).group()
						data['particulate2.5'] = int(num)
						#If data not updated will save the Standard
						flag_val+=1
				except:
					continue
pprint.pprint(data)