#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import re
import pprint
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class Pollution(object):
	def __init__(self, location):
		self.location = location
		self.date = None
		self.standard = {u"ozone" : 180,u"particulate2.5": 100,u"particulate10": 60}
		self.data =  {
						u"place" : unicode(self.location),
						u"ozone" : None,
						u"dateExtracted" : datetime(2015,1,1,0,0),
						u"unit" : u'\u03bc' + u'g/m'+ u'\xb3',
						u"particulate2.5" : None,
						u"particulate10" : None,
	    			}

		self.month = {
						'January' : 1, 'February': 2 ,'March' : 3,
            			'April':4, 'May':5, 'June':6,
            			'July':7,'August':8,'September':9,
            			'October':10,'November':11,'December':12
        			}
	def getStandard(self):
		return self.standard

	def getURL(self):
		pass
	
	def saveHTML(self,r):
		pass
	
	def getHTML(self):
		pass

	def getData(self):
		pass

	def sendmessage(self):
		pass 

	def getLocation(self):
		return self.location

	def getDate(self):
		pass

	def __str__(self):
		pprint.pprint(self.data)
		return self.location


class DelhiPollution(Pollution):
	def __init__(self,location):
		self.location = location
		Pollution.__init__(self,location)
		self.urls = {
			"RK Puram" : "http://www.dpccairdata.com/dpccairdata/display/rkPuramView15MinData.php",
			"Mandir Marg" : "http://www.dpccairdata.com/dpccairdata/display/mmView15MinData.php",
			"Punjabi Bagh" : "http://www.dpccairdata.com/dpccairdata/display/pbView15MinData.php",
			"Anand Vihar" : "http://www.dpccairdata.com/dpccairdata/display/avView15MinData.php"
		}
	def getLocation(self):
		return self.data['place']
	def getData(self):
		url =  self.urls[self.location]
		r = ""
		while True:
			try:
				r = requests.get(url)
				break
			except:
				print "Error in Connection"
				print "RETRYING TO CONNECT TO SERVER" 
				continue
		#Initialize HTML parser
		soup = BeautifulSoup(r.text)
		#Find data with class feild.
		elements_1 =  soup.find_all('tr',class_='tdcolor1')
		elements_2 =  soup.find_all('tr',class_='tdcolor2')

		#GET date and time.
		for td in elements_1:
			flag_str = 0
			date = []
			for i in td:
				nav_text = i.string
				word =  unicode(nav_text)
				if nav_text!="Ozone" and flag_str==0:
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
							date.append(self.month[m])
							date.append(int(d))
						else:
							h,mi,s =  map(int,word.strip().split(":"))
							date.append(h)
							date.append(mi)
							date.append(s)
					continue		
			if len(date)>0:
				self.date = datetime(date[0],date[1],date[2],date[3],date[4],date[5])
				self.data['dateExtracted'] = self.date
			
		#Get value for Ozone.
		for td in elements_1:
			flag_val = 0
			flag_str = 0
			for i in td:
				nav_text = i.string
				word =  unicode(nav_text)
				if re.search(r'Ozone',word):
					flag_str+=1
					continue
				if flag_str==1 and nav_text==None:
					for k in i:
						try:
							val = unicode(k)
							if flag_val==0 and re.search(r"\d+",val):	
								num = re.search(r"\d+\.\d",val).group()
								self.data['ozone'] = float(num)
								#If data not updated will save the Standard
								flag_val+=1
						except:
								continue

		#GET particulate10 value.
		for td in elements_1:
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
									self.data['particulate10'] = int(num)
									#If data not updated will save the Standard
									flag_val+=1
						except:
								continue
		#GET Particulate2.5 value
		for td in elements_2:
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
								self.data['particulate2.5'] = int(num)
								#If data not updated will save the Standard
								flag_val+=1
						except:
							continue

		return self.data