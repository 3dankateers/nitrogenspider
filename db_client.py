#####################################################################
## mondodb api
## db: nitrogen
##
## collection: odds
## odd SCHEMA: id, team1, team2, match_date, ML_T1, ML_T2, date_scraped
#####################################################################

from pymongo import MongoClient

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

	## create new tournament based on model passed in
	def create_tournament(self, name):
		record = self.db.tournaments.insert_one({
			"name" : name}
			)
		return record
	
	## create new match based on model passed in
	def create_match(self, tournament_id, team1, team2, match_date):
		record = self.db.matches.insert_one({
			"tournament_id" : tournament_id,
			"team1" : team1,
			"team2" : team2,
			"match_date" : match_date}
			)
		return record
	
	## create new odd based on odd passed in
	def create_odd(self, match_id, ML_T1, ML_T2, date_scraped):
		record = self.db.odds.insert_one({
			"match_id" : match_id,
			"ML_T1" : ML_T1,
			"ML_T2" : ML_T2,
			"date_scraped" : date_scraped}
			)
		return record
	
	## update existing tournament with new values passed in
	def update_tournament(self, r):
		self.db.tournaments.update_one(
				{"_id" : r.id},{
					"$set": {
						"name" : r.name}
				})
	
	## update existing match with new values passed in
	def update_match(self, r):
		self.db.matches.update_one(
				{"_id" : r.id},{
					"$set": {
						"tournament_id" : r.tournament_id,
						"team1" : r.team1,
						"team2" : r.team2,
						"match_date" : r.match_date}
				})
				
	## update existing odd with new values from odd passed in
	def update_odd(self, r):
		self.db.odds.update_one(
				{"_id" : r.id},{
					"$set": {
						"match_id" : r.match_id,
						"ML_T1" : r.ML_T1,
						"ML_T2" : r.ML_T2,
						"date_scraped" : r.date_scraped}
				})


	## return cursor to odd found based on id
	def get_odd(self, id):
		cursor = self.db.odds.find({"_id" : id})
		return cursor
		
	## return cursor to match found based on id
	def get_match(self, id):
		cursor = self.db.matches.find({"_id" : id})
		return cursor

	## find match that has same teams and date
	def find_match(self, team1, team2, match_date):
		cursor = self.db.matches.find({"team1" : team1, "team2" : team2, "match_date" : match_date})
		return cursor

	## find tournament that has same name 
	def find_tournament(self, name):
		cursor = self.db.tournaments.find({"name" : name})
		return cursor

	## return cursor to tournament found based on id
	def get_tournament(self, id):
		cursor = self.db.tournaments.find({"_id" : id})
		return cursor

