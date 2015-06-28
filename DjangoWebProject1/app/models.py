"""
Definition of models.
"""

from django.db import models
import requests, xmltodict, shutil
from requests.auth import HTTPBasicAuth
from elasticsearch import Elasticsearch
from json import loads, dumps

# Create your models here.

class HotelES:
	def __init__(self, index="hotel"):
		self.index = index
		self.es = Elasticsearch(
				"http://ec2-52-16-231-133.eu-west-1.compute.amazonaws.com:9200/",
				http_auth=('es_admin', 'szelee'),
				verify_certs=False
			)

	def bulkUpdate(self, index, action, doctype="NL"):
		#print "in bulk update"
		#print json.dumps(index) + "\n" + json.dumps(action) + "\n"
		try:
			#print "update data %s" % str(index)
			return self.es.bulk(body=dumps(index) + "\n" + dumps(action) + "\n", index=self.index, doc_type=doctype, refresh=True)
		except Exception as e:
			raise e

	def queryName(self, venue_name):
		specs='{"query":{"bool":{"must":[{"match":{"doc.result.item.name":"'+ venue_name +'"}},{"match":{"doc.result.item.city":"Amsterdam"}}]}},size:1}'
		result = self.es.search(index=self.index, doc_type='NL', body=specs)
		if result['hits']['total'] > 0:
			return result['hits']['hits'][0]['_source']['doc']['result']['item'], result['hits']['hits'][0]['_source']['desc']['result']['item']['texts']['text']['sections']['section']
		else:
			return False, False

	def returnAll(self):
		specs='{"query":{"match_all":{}},"size":1135}'
		result = self.es.search(index=self.index, doc_type='NL', body=specs)
		if result['hits']['total'] > 0:
			return result['hits']['hits']
		else:
			return False

	def queryId(self, venue_id):
		specs='{"query":{"match_phrase":{"doc.result.item.@giataId":"' + venue_id + '"}},"size":1}'
		result = self.es.search(index=self.index, doc_type='NL', body=specs)
		if result['hits']['total'] > 0:
			return result['hits']['hits'][0]['_id']
		else:
			return False, False
		
def loadData():
	f = open("location.txt")
	data = f.readlines()
	f.close()

	es = HotelES()
	new_index = {"index" : {"_index" : "hotel" , "_type" : 'NL'}}
	for each in data:
		url = each.strip('\n')
		response = requests.get(url, auth=HTTPBasicAuth("ghgml|hackathon.com","b3sW7nob"))

		if response.status_code == 200:
			data = loads(dumps(xmltodict.parse(response.text)))
			action = {"doc" : data }
			try:
				#return action
				es.bulkUpdate(new_index, action)
			except Exception as e:
				print e
		else:
			print "data not found"

def updateData(datatype):
	es = HotelES()
	data = es.returnAll()
	for each in data:
		try:
			if datatype == "photo":
				loadPhotos(each['_source']['doc']['result']['item']["@giataId"], each['_source']['doc']['result']['item']["images"]["image"])	 
			else:
				loadText(each['_source']['doc']['result']['item']["@giataId"], each['_source']['doc']['result']['item']["texts"]["text"])
		except Exception as e:
			print "not found %s" % each['_source']['doc']['result']['item']["@giataId"]
			print e.message

def loadText(id, textstring):
	es = HotelES()
	string_link = False
	for each in textstring:
		#print each["@type"]
		if each["@lang"] == "en":
			string_link = each["@xlink:href"]
			print string_link
			venue_id = es.queryId(id)
			print venue_id
			update_index = {"update" : {"_index" : 'hotel', "_type" : 'NL' , "_id" : venue_id }}
		
			if string_link:		
				response = requests.get(string_link, auth=HTTPBasicAuth("ghgml|hackathon.com","b3sW7nob"))
				if response.status_code == 200:
					print "loading"
					data = loads(dumps(xmltodict.parse(response.text)))
					action = {"doc" : {"desc": data} }
					try:
						#return action
						es.bulkUpdate(update_index, action)
					except Exception as e:
						print e
				else:
					print "not loaded"
	
def loadPhotos(id,imagestring):
	image_link = False
	for each in imagestring:
		#print each["@type"]
		if each["@type"] == "w":
			for img in each["sizes"]['size']:
				#print img
				if img["@width"] == "320":
					image_link = img["@xlink:href"]
					break
		elif each["@type"] == "l":
			for img in each["sizes"]['size']:
				#print img
				if img["@width"] == "320":
					image_link = img["@xlink:href"]
					break

		if image_link:		
			response = requests.get(image_link, auth=HTTPBasicAuth("ghgml|hackathon.com","b3sW7nob"), stream=True)
			if response.status_code == 200:
				with open('app/static/app/media/' + str(id) + ".jpg", 'wb') as out_file:
					shutil.copyfileobj(response.raw, out_file)
				del response
				image_link = False