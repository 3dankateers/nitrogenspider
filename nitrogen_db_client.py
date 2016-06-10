#####################################################################
## mondodb api
## db: nitrogen
##
## collection: odds
## odd SCHEMA: id, team1, team2, match_date, ML_T1, ML_T2, date_scraped
#####################################################################

from pymongo import MongoClient

class NitrogenDbClient:
	MONGO_USERNAME = 'root'
	MONGO_PASSWORD = 'm6E7K1GLwcz58q'

	client = None
	db = None
	
	@staticmethod
	def get_client():
		if NitrogenDbClient.client == None:
			NitrogenDbClient.client = MongoClient("mongodb://54.191.167.105:27017")
			NitrogenDbClient.db = NitrogenDbClient.client.nitrogen
			NitrogenDbClient.db.authenticate(NitrogenDbClient.MONGO_USERNAME, NitrogenDbClient.MONGO_PASSWORD, source='admin')
		return NitrogenDbClient.client

	@staticmethod
	def get_db():
		if NitrogenDbClient.client == None:
			NitrogenDbClient.client = MongoClient("mongodb://54.191.167.105:27017")
			NitrogenDbClient.db = NitrogenDbClient.client.nitrogen
			NitrogenDbClient.db.authenticate(NitrogenDbClient.MONGO_USERNAME, NitrogenDbClient.MONGO_PASSWORD, source='admin')
		return NitrogenDbClient.db
