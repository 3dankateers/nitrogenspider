## Model for match
## matches: id, tournament_id, team1, team2, match_date, match_day

from nitrogen_db_client import NitrogenDbClient

class ProMatch:
	def __init__(self, tournament_id, team1, team2, match_date, match_day, id = None):
		self.id = id
		self.tournament_id = tournament_id
		self.team1 = team1
		self.team2 = team2
		self.match_date = match_date
		self.match_day = match_day
	
	##constructor from Cursor
	@classmethod
	def from_cursor(cls, c):
		assert (c.count() == 1), "Error constructing Match model from cursor. Cursor is empty or contains multiple objects"
		id = c[0]["_id"]
		tournament_id = c[0]["tournament_id"]
		team1 = c[0]["team1"]
		team2 = c[0]["team2"]
		match_date = c[0]["match_date"]
		match_day = c[0]["match_day"]
		return cls(tournament_id, team1, team2, match_day, id)
	
	@classmethod
	def find_match(cls, tournament_id, team1, team2, match_date, match_day):
		cursor = cls.lookup_match(team1,team2, match_day)
		
		if cursor.count() == 0:
			return cls(tournament_id, team1, team2 ,match_date, match_day)
		else:
			return cls.from_cursor(cursor)
	
	## create new match based on model passed in
	@staticmethod
	def create_match(tournament_id, team1, team2, match_date, match_day):
		record = NitrogenDbClient.get_db().matches.insert_one({
			"tournament_id" : tournament_id,
			"team1" : team1,
			"team2" : team2,
			"match_date" : match_date,
			"match_day" : match_day}
			)
		return record.inserted_id
	
	## update existing match with new values passed in
	@staticmethod
	def update_match(id, tournament_id, team1, team2, match_date, match_day):
		NitrogenDbClient.get_db().matches.update_one(
				{"_id" : id},{
					"$set": {
						"tournament_id" : tournament_id,
						"team1" : team1,
						"team2" : team2,
						"match_date" : match_date,
						"match_day" : match_day}
				})

	## return cursor to match found based on id
	@staticmethod
	def get_match(id):
		cursor = NitrogenDbClient.get_db().matches.find({"_id" : id})
		return cursor

	## find match that has same teams and date
	@staticmethod
	def lookup_match(team1, team2, match_day):
		cursor = NitrogenDbClient.get_db().matches.find({"team1" : team1, "team2" : team2, "match_day" : match_day})
		return cursor


	def save(self):
		##if found already in db
		if self.id != None:
			##print "old"
			ProMatch.update_match(self.id, self.tournament_id, self.team1, self.team2, self.match_date, self.match_day)
		## else it's a new odd that needs to be created
		else:
			##print "new"
			self.id = ProMatch.create_match(self.tournament_id, self.team1, self.team2, self.match_date, self.match_day)

