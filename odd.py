## Model for odd
## odds: id, team1, team2, match_date, ML_T1, ML_T2, date_scraped

from db_client import DbClient


class Odd:
	def __init__(self, id, team1, team2, match_date, ML_T1, ML_T2, date_scraped):
		self.id = id
		self.team1 = team1
		self.team2 = team2
		self.match_date = match_date
		self.ML_T1 = ML_T1
		self.ML_T2 = ML_T2
		self.date_scraped = date_scraped
	
	##constructor from Cursor
	@classmethod
	fromCursor(cls, c):
		assert (len(c) == 1), "Error constructing Odd model from cursor. Cursor is empty or contains multiple objects"
		id = c[0]["_id"]
		team1 = c[0]["team1"]
		team2 = c[0]["team2"]
		match_date = c[0]["match-date"]
		ML_T1 = c[0]["ML_T1"]
		ML_T2 = c[0]["ML_T2"]
		date_scraped = c[0]["date_scraped"]
		return cls(id, team1, team2, match_date, ML_T1, ML_T2, date_scraped)

	def save(self):
		with db_client as DbClient:
			cursor = db_client.get_odd(id)
			##if found already in db
			if cursor.count() == 1:
				db_client.update_odd(self)					
			## else it's a new odd that needs to be created
			else:
				db_client.create_odd(self)

			


