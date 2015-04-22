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

