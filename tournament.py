## Model for tournamnet
## tournament: id, name

from nitrogen_db_client import NitrogenDbClient

class Tournament:
	def __init__(self, name, id = None):
		self.id = id 
		self.name = name
	
	##constructor from dict
	@classmethod
	def from_dict(cls, d):
		id = d["_id"]
		name = d["name"]
		return cls(name, id)
	
	## either returns existing tournament or returns a new one
	@classmethod
	def find_tournament(cls, name):
		cursor = cls.lookup_tournament(name)
		if cursor.count() == 0:
			return cls(name)
		else:
			return cls.from_cursor(cursor)
	
	## create new tournament based on model passed in
	@staticmethod
	def create_tournament (name):
		record = NitrogenDbClient.get_db().tournaments.insert_one({
			"name" : name}
			)
		return record.inserted_id
	
	## update existing tournament with new values passed in
	@staticmethod
	def update_tournament(id, name):
		NitrogenDbClient.get_db().tournaments.update_one(
				{"_id" : id},{
					"$set": {
						"name" : name}
				})
	
	## find tournament that has same name 
	@staticmethod
	def lookup_tournament(name):
		cursor = NitrogenDbClient.get_db().tournaments.find({"name" : name})
		return cursor

	## return cursor to tournament found based on id
	@staticmethod
	def get_tournament(id):
		cursor = NitrogenDbClient.get_db().tournaments.find({"_id" : id})
		return cursor

	## return cursor to tournament found based on id
	@staticmethod
	def get_all():
		cursor = NitrogenDbClient.get_db().tournaments.find()
		return cursor
	
	def save(self):
		##if found already in db
		if self.id != None:
			Tournament.update_tournament(self.id, self.name)					
		## else it's a new odd that needs to be created
		else:
			self.id = Tournament.create_tournament(self.name)

