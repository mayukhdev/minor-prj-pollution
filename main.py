#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Usage: main.py

Initilizes Server
Extracts data from Pollution and formats it to be stored in the database.
Inserts into database
"""
from Server.DelhiPollution import DelhiPollution
import sys
from Database import *
from time import sleep

class ServerExtract(object):
	def __init__(self):
		self.database_insert = Database()
	def Extract(self): 
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

		self.database_insert.insert_data(data_audit)
		

if __name__=="__main__":
	try:
		extract = ServerExtract()
		print "Server Initiated"
		while True:
			extract.Extract()
			sleep(20*60)
	except KeyboardInterrupt:
		print "Server Stopped"
	except:
		print sys.exc_info()[0]
	finally:		
		print "Bye"