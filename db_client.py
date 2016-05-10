#####################################################################
## mondodb api
## db: nitrogen
##
## collection: odds
## odd SCHEMA: id, team1, team2, match_date, ML_T1, ML_T2, date_scraped
#####################################################################

##TODO rename match to odds or something better

from odd import Odd


class DbClient:
	MONGO_USERNAME = 'root'
	MONGO_PASSWORD = 'm6E7K1GLwcz58q'

	def __init__(self):
		self.client = MongoClient("mongodb://54.191.167.105:27017")
		self.db = self.client.nirogen
		self.db.authenticate(self.MONGO_USERNAME, self.MONGO_PASSWORD, source='admin')
	
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_value, tb):
		self.client.close()

	## update existing odd with new values from odd passed in
	def update_odd(self, o):
		self.db.odds.update_one(
				{"_id" : o.id},{
					"$set": {
						"team1" : o.team1,
						"team2" : o.team2,
						"match_date" : o.match_date,
						"ML_T1" : o.ML_T1,
						"ML_T2" : o.ML_T2,
						"date_scraped" : o.date_scraped}
				})

	## create new odd based on odd passed in
	def create_odd(self, o):
		record = self.db.odds.insert_one({
			"team1" : o.team1,
			"team2" : o.team2,
			"match_date" : o.match_date,
			"ML_T1" : o.ML_T1,
			"ML_T2" : o.ML_T2,
			"date_scraped" : o.date_scraped}
			})

	## return cursor to odd found based on id
	def get_odd(self, id):
		cursor = self.db.odds.find({"_id" : id})
		return cursor
		


