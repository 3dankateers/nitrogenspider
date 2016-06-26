from nitrogen_db_client import NitrogenDbClient
from odd import Odd
from pro_match import ProMatch 

def embed_all():
	cursor = ProMatch.get_all_matches()
	print cursor.count()
	for m in cursor:
		print "here"
		match = ProMatch.from_dict(m)
		odds_cursor = Odd.get_odds_for_match(match.id)
		for o in odds_cursor:
			match.odds.append(o)
		match.save()
embed_all()


