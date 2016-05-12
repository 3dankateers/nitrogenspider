## Model for match
## matches: id, tournament_id, team1, team2, match_date

from db_client import DbClient

class Match:
	def __init__(self, tournament_id, team1, team2, match_date, id = None):
		self.id = id
		self.tournament_id = tournament_id
		self.team1 = team1
		self.team2 = team2
		self.match_date = match_date
	
	##constructor from Cursor
	@classmethod
	def from_cursor(cls, c):
		assert (c.count() == 1), "Error constructing Match model from cursor. Cursor is empty or contains multiple objects"
		id = c[0]["_id"]
		tournament_id = c[0]["tournament_id"]
		team1 = c[0]["team1"]
		team2 = c[0]["team2"]
		match_date = c[0]["match_date"]
		return cls(tournament_id, team1, team2, match_date, id)
	
	@classmethod
	def find_match(cls, tournament_id, team1, team2, match_date):
		with DbClient() as db_client:
			cursor = db_client.find_match(team1,team2, match_date)
			if cursor.count() == 0:
				return cls(tournament_id, team1, team2, match_date)
			else:
				return cls.from_cursor(cursor)


	def save(self):
		with DbClient() as db_client:
			##if found already in db
			if self.id != None:
				##print "old"
				db_client.update_match(self)
			## else it's a new odd that needs to be created
			else:
				##print "new"
				self.id = db_client.create_match(self.tournament_id, self.team1, self.team2, self.match_date)

