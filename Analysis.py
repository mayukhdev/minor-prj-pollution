#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Database import find_data
from datetime import datetime
import pprint
import sys
import pylab as pl

def showPlotMul(elements,location,time,data):
	"""Only 1 element """
	if len(elements)>1:
		return
	#fig = pl.figure()
	#ax = fig.add_subplot(111)
	place = {}
	for l in location:
		values = {
				'ozone' : [],
				'particulate2' : [],
				'particulate10' : [],
				'date' : []
		}
		place[l] = values
	for e in elements:
		for d in data:
			flag = 0
			for l in location:
				if d['location'][l][e] == None:
					flag = 1
					break
			if flag==0:
				#print "INputting"
				#pprint.pprint(d)			
				for l in location:
					place[l][e].append(d['location'][l][e])
					place[l]['date'].append(d['date'])
	
	#print "HERE"
	pprint.pprint(place)

def showPlot(elements,location,time,data):
	fig = pl.figure()
	ax = fig.add_subplot(111)
	if len(elements)>1:
		print "Only one element"
		return
	n = len(location) #Assume n = 1
	l = 0
	ozone_standard = 180
	particulate2_standard = 60
	particulate10_standard = 100
	if n==1:
		date = []
		ozone = []
		standard = []
		particulate10 = []
		particulate2 = []
		for i in data:
			if elements[0]=='ozone':
				if i['location'][location[l]]['ozone'] != None:
					ozone.append(i['location'][location[l]]['ozone'])
					date.append(i['date'])
					standard.append(ozone_standard)
			elif elements[0]=='particulate10':
				if i['location'][location[l]]['particulate10'] != None:
					particulate10.append(i['location'][location[l]]['particulate10'])
					date.append(i['date'])
					standard.append(particulate10_standard)
			else:
				if i['location'][location[l]]['particulate2'] != None:
					particulate2.append(i['location'][location[l]]['particulate2'])
					date.append(i['date'])
					standard.append(particulate2_standard)
		
		if elements[0]=='ozone':
			std = pl.plot(range(len(standard)),standard,color='red')
			oz = ax.plot(range(len(ozone)),ozone,color='black')
			ax.set_ylabel(u"Ozone "+'u' + u'g/m'+ u'\xb3')
			ax.set_title('Ozone in {0}'.format(location[l]))
			ax.set_xticks(range(len(ozone)))
			xtickNames = ax.set_xticklabels(date,rotation=90)	
			#pl.legend(std,("Standard",),loc='best')
			pl.legend((std[0],oz[0]),("Ozone","Standard"),loc='best')
			pl.setp(xtickNames)
		elif elements[0]=='particulate10':
			std = pl.plot(range(len(standard)),standard,color='red')
			p10 = ax.plot(range(len(particulate10)),particulate10,color='black')
			ax.set_ylabel(u"Particulate < 10 "+'u' + u'g/m'+ u'\xb3')
			ax.set_title('Particulate < 10 in {0}'.format(location[l]))
			ax.set_xticks(range(len(particulate10)))
			xtickNames = ax.set_xticklabels(date,rotation=90)	
			pl.legend((std[0],p10[0]),("Standard","Particulate < 10"),loc='best')
			pl.setp(xtickNames)
		else:
			std = pl.plot(range(len(standard)),standard,color='red')
			p10 = ax.plot(range(len(particulate2)),particulate2,color='black')
			ax.set_ylabel(u"Particulate < 2 "+'u' + u'g/m'+ u'\xb3')
			ax.set_title('Particulate < 10 in {0}'.format(location[l]))
			ax.set_xticks(range(len(particulate2)))
			xtickNames = ax.set_xticklabels(date,rotation=90)	
			pl.legend((std[0],p10[0]),("Standard","Particulate < 2"),loc='best')
			pl.setp(xtickNames)

	pl.show()

def get_data(q):
	elements = []
	counter = 0
	for i in range(len(q)):
		if q[i]=='in' or q[i] in ['*','all']:
			if q[i] in ['*','all']:
				elements.extend(['ozone','particulate10','particulate2'])
				counter = i+2
			else:
				counter = i+1
			break
		if q[i] not in ['ozone','particulate10','particulate2']:
			print 'Element error'
			return 0
		elements.append(q[i])
	location = []
	for j in range(counter,len(q)):
		if q[j] in ['from','till']:
			counter = j
			break
		if q[j]=="*":
			location.extend(['Anand Vihar','Punjabi Bagh','RK Puram','Mandir Marg'])
			break
		temp = q[j]
		if q[j]=='AV':
			temp = 'Anand Vihar'
		elif q[j]=='PB':
			temp = 'Punjabi Bagh'
		elif q[j] in ['RKP','RK']:
			temp = 'RK Puram'
		elif q[j]=='MM':
			temp = 'Mandir Marg'
		else:
			print 'Location error'
			return 0
		location.append(temp)
	#NOW
	time = datetime.today()
	print elements,location,time

	if len(location)==1:
		data = []
		for l in location:		
			for e in elements:
				to_find = 'location.' + l + "." + e
				query = {
							'date' : {'$lte': time}
				}
				d =  find_data(query,
						proj={to_find:1,'_id':0,'date':1,}
						,sort = 1)					
				for i in d:
					data.append(i)
		for j in data:
			pprint.pprint(j)
		showPlot(elements,location,time,data)
	else:
		d = find_data({'date': {'$lte' : time}})
		# for i in d:
		# 	pprint.pprint(i)
		showPlotMul(elements,location,time,d)
	return 1

def main():
	#q = {"date":datetime(2015,04,23,15,10)}
	#find_data(q)[0]
	while True:
		print ""
		print "Elements = ozone , particulate10 , particulate2"
		print "Location = RK: RK Puram , MM: Mandir Marg , AV: Anand Vihar, PB: Punjabi Bagh"
		print "Quit = q"
		print "Enter Query:",
		try:
			s = raw_input()
			if s in ["quit","q",'exit']:
				break
			query = s.split()
		
			if query[0]=='get':
				check = get_data(query[1:])
				if check==0:
					print "Error in Query"
					continue
		except:
			continue
	print "Bye"

if __name__ == '__main__':
	main()