#####################################################################
## mondodb api
## db: nitrogen
##
## collection: odds
## odd SCHEMA: id, team1, team2, match_date, ML_T1, ML_T2, date_scraped
#####################################################################

from pymongo import MongoClient

class DbClient:

	def __init__(self):
		self.client = MongoClient("mongodb://localhost:27017/")
		self.db = self.client.nitrogen
	
	def __enter__(self):
		return self
	
	def __exit__(self, exc_type, exc_value, tb):
		self.client.close()

	## create new tournament based on model passed in
	def create_tournament(self, name):
		record = self.db.tournaments.insert_one({
			"name" : name}
			)
		return record.inserted_id
	
	## create new match based on model passed in
	def create_match(self, tournament_id, team1, team2, match_date):
		record = self.db.matches.insert_one({
			"tournament_id" : tournament_id,
			"team1" : team1,
			"team2" : team2,
			"match_date" : match_date}
			)
		return record.inserted_id
	
	## create new odd based on odd passed in
	def create_odd(self, match_id, ML_T1, ML_T2, date_scraped):
		record = self.db.odds.insert_one({
			"match_id" : match_id,
			"ML_T1" : ML_T1,
			"ML_T2" : ML_T2,
			"date_scraped" : date_scraped}
			)
		return record.inserted_id
	
	## update existing tournament with new values passed in
	def update_tournament(self, id, name):
		self.db.tournaments.update_one(
				{"_id" : id},{
					"$set": {
						"name" : name}
				})
	
	## update existing match with new values passed in
	def update_match(self, id, tournament_id, team1, team2, match_date):
		self.db.matches.update_one(
				{"_id" : id},{
					"$set": {
						"tournament_id" : tournament_id,
						"team1" : team1,
						"team2" : team2,
						"match_date" : match_date}
				})
				
	## update existing odd with new values from odd passed in
	def update_odd(self, id, match_id, ML_T1, ML_T2, date_scraped):
		self.db.odds.update_one(
				{"_id" : id},{
					"$set": {
						"match_id" : match_id,
						"ML_T1" : ML_T1,
						"ML_T2" : ML_T2,
						"date_scraped" : date_scraped}
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
