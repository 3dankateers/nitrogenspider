## Model for odd
## odds: id, match_id, ML_T1, ML_T2, date_scraped

from db_client import DbClient
import time
import datetime

class Odd:
	def __init__(self, match_id, ML_T1, ML_T2, date_scraped, id = None):
		self.id = id
		self.match_id = match_id
		self.ML_T1 = ML_T1
		self.ML_T2 = ML_T2
		self.date_scraped = date_scraped
	
	##constructor from Cursor
	@classmethod
	def from_cursor(cls, c):
		assert (c.count() == 1), "Error constructing Odd model from cursor. Cursor is empty or contains multiple objects"
		id = c[0]["_id"]
		match_id = c[0]["match_id"]
		ML_T1 = c[0]["ML_T1"]
		ML_T2 = c[0]["ML_T2"]
		date_scraped = c[0]["date_scraped"]
		return cls(match_id, ML_T1, ML_T2, date_scraped, id)

	def save(self):
		with DbClient() as db_client:	
			##if found already in db
			if self.id != None:
				db_client.update_odd(self.id, self.match_id, self.ML_T1, self.ML_T1, self.date_scraped)					
			## else it's a new odd that needs to be created
			else:
				print self.match_id
				self.id = db_client.create_odd(self.match_id, self.ML_T1, self.ML_T2, self.date_scraped)

