from pymongo import MongoClient
import json 
import pprint
import sys

class Database(object):
	def __init__(self):
		try:
			self.client = MongoClient("mongodb://localhost:27017/")
			self.db = self.client.pollution
		except:
			print "Please run the server!"
			sys.exit()
			self.fixed = None

	def insert_data(self,data):
		self.fixed = self.fix_data_for_insertion(data)
		#pprint.pprint(fixed)
		#print "Trying to insert"
		try: 
			self.find_data({"date":self.fixed["date"]})[0]
		except:
			print "Data Inserted"
			self.db.data.insert(self.fixed)
			

	def fix_data_for_insertion(self,data):
		data_format = {
				"date" : None,
				"location" : {
								"RK Puram" : None,
								"Mandir Marg" : None,
								"Punjabi Bagh" : None,
								"Anand Vihar" : None
				},
				"unit" : None,
				"standard" : {
								u"ozone" : 180,
								u"particulate2": 60,
								u"particulate10": 100
				}
		}
		#pprint.pprint(data)
		data_format["date"] = data["date"]
		data_format["unit"] = data["unit"]
		for loc in data["location"]:
			data_values = {
							"ozone":None,
							"particulate10":None,
							"particulate2":None
			}
			data_values["ozone"] = data["location"][loc]["ozone"]
			
			if data["standard"]["particulate10"]!= data["location"][loc]["particulate10"] or data["standard"]["particulate2"]!= data["location"][loc]["particulate2"]:
				data_values["particulate10"] = data["location"][loc]["particulate10"]
				data_values["particulate2"] = data["location"][loc]["particulate2"]			

			data_format["location"][loc] = data_values

		return data_format



	def find_data(self,query,proj=None,sort=None):
		if proj and sort:
			return self.db.data.find(query,proj).sort([('date',1)]) #get based on time in sorted order
		else:
			return self.db.data.find(query).sort([('date',1)])

	def update_data(self,query):
		pass

	def delete_data(self,query):
		self.db.data.remove(query)