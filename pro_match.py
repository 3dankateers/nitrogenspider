## Model for match
## matches: id, team1_name, team2_name, map_number, match_day, champs1, champs2, win, match_date, is_test, tournament_id, first_blood, kills_5, status
## status possibilities: "nitrogen" or "csv or "both" or None

from nitrogen_db_client import NitrogenDbClient
from odd import Odd


class ProMatch:

	##Required on creation:							team1_name, team2_name, map_number, match_day
	##Possibly populated later by csv file:			champs1, champs2, win, first_blood, kills_5, red_side
	##Possibly populated later by nitrogen scraper: tournament_id, match_date
	## set programmatically:						id, is_test, status

	def __init__(self, team1_name, team2_name, map_number, match_day, red_side = None, champs1 = None, champs2 = None, win = None, match_date = None, is_test = None, tournament_id = None, first_blood = None, kills_5 = None, status = None, id = None):
		self.id = id
		self.team1_name = team1_name
		self.team2_name = team2_name
		self.map_number = map_number
		self.match_day = match_day
		self.red_side = red_side
		self.champs1 = champs1
		self.champs2 = champs2
		self.win = win
		self.match_date = match_date
		self.is_test = is_test
		self.tournament_id = tournament_id
		self.first_blood = first_blood
		self.kills_5 = kills_5
		self.status = status
		self.to_invert = False
	
	##constructor from Cursor
	@classmethod
	def from_dict(cls, c):
		id = c["_id"]
		team1_name = c["team1_name"]
		team2_name = c["team2_name"]
		map_number = c["map_number"]
		match_day = c["match_day"]
		red_side = c["red_side"]
		champs1 = c["champs1"]
		champs2 = c["champs2"]
		win = c["win"]
		match_date = c["match_date"]
		is_test = c["is_test"]
		tournament_id = c["tournament_id"]
		first_blood = c["first_blood"]
		kills_5 = c["kills_5"]
		status = c["status"]
		return cls(team1_name, team2_name, map_number, match_day, red_side, champs1, champs2, win, match_date, is_test, tournament_id, first_blood, kills_5, status, id)
	
	## Uniquely defined by: team1_name, team2_name, map_number, match_day
	## if match already exists in db return it, else create new match using required information
	@classmethod
	def find_match(cls, team1_name, team2_name, map_number, match_day, caller):
		cursor1 = cls.lookup_match(team1_name, team2_name, map_number, match_day)
		cursor2 = cls.lookup_match(team2_name, team1_name, map_number, match_day)

		## pretty sure nitrogen lists teams alphabetically so need to check both since csv find_match uses red_side/blue_side order
		if cursor1.count() != 0:
			##no inversion neccesary
			match = cls.from_dict(cursor1[0])
			match.to_invert = False
			return match
		elif cursor2.count() != 0:
			##inversion might be neccesary
			match = cls.from_dict(cursor2[0])
			match.set_should_invert(caller)
			return match
		else:
			return cls(team1_name, team2_name, map_number, match_day)
	
	## check if inversion neccesary(same match but team1 and team2 are swapped)
	def set_should_invert(self, caller):
		## if both means inversion was done already
		if self.status == "both":
			self.to_invert = False
		elif self.status == caller:
			print "wtf should not be possible"
			self.to_invert = False
		else:
			self.to_invert = True

	## create new match based on model, returns match_id
	def create_match(self):
		record = NitrogenDbClient.get_db().matches.insert_one({
			"team1_name" : self.team1_name,
			"team2_name" : self.team2_name,
			"map_number" : self.map_number,
			"match_day" : self.match_day,
			"red_side" : self.red_side,
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
						"red_side" : self.red_side,
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


	## return all matches not marked as is_test
	@staticmethod
	def get_training_set():
		cursor = NitrogenDbClient.get_db().matches.find({"$or":[ {"status" : "both", "is_test" : False}, {"status" : "csv", "is_test" : False }]})
		return cursor

	## return all matches that are labeled is_test
	@staticmethod
	def get_test_set():
		cursor = NitrogenDbClient.get_db().matches.find({"$or":[ {"status" : "both", "is_test" : True}, {"status" : "csv", "is_test" : True}]})
		return cursor

	##returns all matches that have csv data
	@staticmethod
	def get_csv_set():
		cursor = NitrogenDbClient.get_db().matches.find({"$or":[ {"status" : "both"}, {"status" : "csv"}]})
		return cursor

	@staticmethod
	def get_testable_set():
		cursor = NitrogenDbClient.get_db().matches.find({"$or":[ {"status" : "both"}, {"status" : "csv"}]})
		return cursor

	@staticmethod
	def get_bettable_set():
		cursor = NitrogenDbClient.get_db().matches.find({"status" : "both"})
		return cursor
		

	## return all matches
	@staticmethod
	def get_all_matches():
		cursor = NitrogenDbClient.get_db().league.matches.find()
		return cursor

	def get_latest_ML_T1(self):
		##sorted by date when returned
		cursor = Odd.get_odds_for_match(self.id)
		latest_odd = Odd.from_dict(cursor[0])
		return latest_odd.ML_T1

	def get_latest_ML_T2(self):
		##sorted by date when returned
		cursor = Odd.get_odds_for_match(self.id)
		latest_odd = Odd.from_dict(cursor[0])
		return latest_odd.ML_T2

	def save(self):
		##if found already in db
		if self.id != None:
			##should only ever run once per match(sometimes 0 times)
			if self.to_invert == True:
				self.invert()
			self.update_match()
		## else it's a new odd that needs to be created
		else:
			##print "new"
			self.id = self.create_match()

	##invert teams
	def invert(self):
		assert (self.status == "both")
		print "inverting"
		temp = self.team1_name
		self.team1_name = self.team2_name
		self.team2_name = temp
		ProMatch.invert_value(self.red_side)
		temp = self.champs1
		self.champs1 = self.champs2
		self.champs2 = temp
		ProMatch.invert_value(self.win)
		ProMatch.invert_value(self.first_blood)
		ProMatch.invert_value(self.kills_5)
	
	## 200 becomes 100 and 100 becomes 200
	@staticmethod
	def invert_value(val):
		if val == None:
			return
		elif val == 100:
			val == 200
		else:
			val == 100

