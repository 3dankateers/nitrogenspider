## Model for tournamnet
## tournament: id, name

from db_client import DbClient

class Tournament:
	def __init__(self, name, id = None):
		self.id = id 
		self.name = name
	
	##constructor from Cursor
	@classmethod
	def from_cursor(cls, c):
		assert (c.count() == 1), "Error constructing Tournament model from cursor. Cursor is empty or contains multiple objects"
		id = c[0]["_id"]
		name = c[0]["name"]
		return cls(name, id)
	
	## either returns existing tournament or returns a new one
	@classmethod
	def find_tournament(cls, name):
		with DbClient() as db_client:
			cursor = db_client.find_tournament(name)
			if cursor.count() == 0:
				return cls(name)
			else:
				return cls.from_cursor(cursor)
	
	def save(self):
		with DbClient() as db_client:
			##if found already in db
			if self.id != None:
				db_client.update_tournament(self.id, self.name)					
			## else it's a new odd that needs to be created
			else:
				self.id = db_client.create_tournament(self.name)

