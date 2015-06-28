"""
Definition of models.
"""

from django.db import models
from elasticsearch import Elasticsearch

# Create your models here.

class HotelES:
	def __init__(self, index='hotel'):
		self.index = index
		self.es = Elasticsearch(
				"http://ec2-52-16-231-133.eu-west-1.compute.amazonaws.com:9200/",
				http_auth=('es_admin', 'szelee'),
				verify_certs=False
			)
	
	def getVenueName(self, venue_name):
		specs = '{"query":{"bool":{"must":[{"match":{"doc.result.item.name":"'+ venue_name +'"}},{"match":{"doc.result.item.city":"Amsterdam"}}]}},"size":1}'
		result = self.es.search(index=self.index, doc_type='NL', body=specs)
		if result['hits']['total'] > 0:
			return result['hits']['hits'][0]['_source']['doc']['result']['item'], result['hits']['hits'][0]['_source']['desc']['result']['item']['texts']['text']['sections']['section']
		else:
			return False

	def getVenueID(self, venue_id):
		specs = '{"query":{"match_phrase":{"doc.result.item.@giataId":"' + venue_id + '"}},"size":1}'
		result = self.es.search(index=self.index, doc_type='NL', body=specs)
		if result['hits']['total'] > 0 :
			return result['hits']['hits'][0]['_source']['doc']['result']['item'], result['hits']['hits'][0]['_source']['desc']
		else:
			return False, False