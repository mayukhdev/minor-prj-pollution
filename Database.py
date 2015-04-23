from pymongo import MongoClient
import json 
import pprint

client = MongoClient("mongodb://localhost:27017/")
db = client.pollution

def insert_data(data):
	fixed = fix_data_for_insertion(data)
	#pprint.pprint(fixed)
	print "Trying to insert"
	try: 
		find_data({"date":fixed["date"]})[0]
	except:
		print "Data Inserted"
		db.data.insert(fixed)
		

def fix_data_for_insertion(data):
	
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



def find_data(query):
	return db.data.find(query)

def update_data(query):
	pass

def delete_data(query):
	pass