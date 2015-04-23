#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Pollution import Pollution
from DelhiPollution import DelhiPollution
import pprint
import pylab as pl
import sys
from LatestData import ShowData
from Database import *
from time import sleep

def Extract(): 
	RKP = DelhiPollution("RK Puram")
	PB =  DelhiPollution("Punjabi Bagh")
	AV = DelhiPollution("Anand Vihar")
	MM = DelhiPollution("Mandir Marg")

	data_audit = {
			"date" : RKP.getData()['dateExtracted'],
			"location" : {
							RKP.getLocation() : RKP.getData(),
							PB.getLocation() : PB.getData(),
							AV.getLocation() : AV.getData(),
							MM.getLocation() : MM.getData()
						},
			"unit" : RKP.getData()["unit"],
			"standard" : RKP.getStandard()
		}
	#pprint.pprint(data_audit)
	if len(sys.argv)>1 and sys.argv[1]=="show":
		ShowData(data_audit)

	insert_data(data_audit)
		

if __name__=="__main__":
	print "Server Initiated"
	while True:
		Extract()
		sleep(20*60)