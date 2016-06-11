## Model for match
## matches: id, team1_name, team2_name, map_number, match_day, champs1, champs2, win, match_date, is_test, tournament_id, first_blood, kills_5, status
## status possibilities: "nitrogen" or "csv or "both" or None

from nitrogen_db_client import NitrogenDbClient

class ProMatch:

	##Required on creation:							team1_name, team2_name, map_number, match_day
	##Possibly populated later by csv file:			champs1, champs2, win, first_blood, kills_5
	##Possibly populated later by nitrogen scraper: tournament_id, match_date
	## set programmatically:						id, is_test, status

	def __init__(self, team1_name, team2_name, map_number, match_day, champs1 = None, champs2 = None, win = None, match_date = None, is_test = True, tournament_id = None, first_blood = None, kills_5 = None, status = None, id = None):
		self.id = id
		self.team1_name = team1_name
		self.team2_name = team2_name
		self.map_number = map_number
		self.match_day = match_day
		self.champs1 = champs1
		self.champs2 = champs2
		self.win = win
		self.match_date = match_date
		self.is_test = is_test
		self.tournament_id = tournament_id
		self.first_blood = first_blood
		self.kills_5 = kills_5
		self.status = status
	
	##constructor from Cursor
	@classmethod
	def from_cursor(cls, c):
		assert (c.count() == 1), "Error constructing Match model from cursor. Cursor is empty or contains multiple objects"
		id = c[0]["_id"]
		team1_name = c[0]["team1_name"]
		team2_name = c[0]["team2_name"]
		map_number = c[0]["map_number"]
		match_day = c[0]["match_day"]
		champs1 = c[0]["champs1"]
		champs2 = c[0]["champs2"]
		win = c[0]["win"]
		match_date = c[0]["match_date"]
		is_test = c[0]["is_test"]
		tournament_id = c[0]["tournament_id"]
		first_blood = c[0]["first_blood"]
		kills_5 = c[0]["kills_5"]
		status = c[0]["status"]
		return cls(team1_name, team2_name, map_number, match_day, champs1, champs2, win, match_date, is_test, tournament_id, first_blood, kills_5, status, id)
	
	## Uniquely defined by: team1_name, team2_name, map_number, match_day
	## if match already exists in db return it, else create new match using required information
	@classmethod
	def find_match(cls, team1_name, team2_name, map_number, match_day):
		cursor = cls.lookup_match(team1_name, team2_name, map_number, match_day)
		
		if cursor.count() == 0:
			return cls(team1_name, team2_name, map_number, match_day)
		else:
			return cls.from_cursor(cursor)
	
	## create new match based on model, returns match_id
	def create_match(self):
		record = NitrogenDbClient.get_db().matches.insert_one({
			"team1_name" : self.team1_name,
			"team2_name" : self.team2_name,
			"map_number" : self.map_number,
			"match_day" : self.match_day,
			"champs1" : self.champs1,
			"champs2" : self.champs2,
			"win" : self.win,
			"match_date" : self.match_date,
			"is_test" : self.is_test,
			"tournament_id" : self.tournament_id,
			"first_blood" : self.first_blood,
			"kills_5" : self.kills_5,
			"status" : self.status
			})
		return record.inserted_id
	
	## update existing match with new values in model
	def update_match(self):
		NitrogenDbClient.get_db().matches.update_one(
				{"_id" : self.id},{
					"$set": {
						"team1_name" : self.team1_name,
						"team2_name" : self.team2_name,
						"map_number" : self.map_number,
						"match_day" : self.match_day,
						"champs1" : self.champs1,
						"champs2" : self.champs2,
						"win" : self.win,
						"match_date" : self.match_date,
						"is_test" : self.is_test,
						"tournament_id" : self.tournament_id,
						"first_blood" : self.first_blood,
						"kills_5" : self.kills_5,
						"status" : self.status 
						}
				})

	## return cursor to match found based on id
	@staticmethod
	def get_match(id):
		cursor = NitrogenDbClient.get_db().matches.find({"_id" : id})
		return cursor

	## find match that has same teams and date
	@staticmethod
	def lookup_match(team1_name, team2_name, map_number, match_day):
		cursor = NitrogenDbClient.get_db().matches.find({"team1_name" : team1_name, "team2_name" : team2_name, "map_number" : map_number, "match_day" : match_day})
		return cursor


	def save(self):
		##if found already in db
		if self.id != None:
			self.update_match()
		## else it's a new odd that needs to be created
		else:
			##print "new"
			self.id = self.create_match()

