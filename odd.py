## Model for odd
## odds: id, match_id, ML_T1, ML_T2, date_scraped

from nitrogen_db_client import NitrogenDbClient
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
		##if found already in db
		if self.id != None:
			Odd.update_odd(self.id, self.match_id, self.ML_T1, self.ML_T1, self.date_scraped)					
		## else it's a new odd that needs to be created
		else:
			print self.match_id
			self.id = Odd.create_odd(self.match_id, self.ML_T1, self.ML_T2, self.date_scraped)

	## create new odd based on odd passed in
	@staticmethod
	def create_odd(match_id, ML_T1, ML_T2, date_scraped):
		record = NitrogenDbClient.get_db().odds.insert_one({
			"match_id" : match_id,
			"ML_T1" : ML_T1,
			"ML_T2" : ML_T2,
			"date_scraped" : date_scraped}
			)
		return record.inserted_id
	
	## update existing odd with new values from odd passed in
	@staticmethod
	def update_odd(id, match_id, ML_T1, ML_T2, date_scraped):
		NitrogenDbClient.get_db().odds.update_one(
				{"_id" : id},{
					"$set": {
						"match_id" : match_id,
						"ML_T1" : ML_T1,
						"ML_T2" : ML_T2,
						"date_scraped" : date_scraped}
				})
	
	## return cursor to odd found based on id
	@staticmethod
	def get_odd(id):
		cursor = NitrogenDbClient.get_db().odds.find({"_id" : id})
		return cursor

