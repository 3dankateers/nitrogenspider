from tournament import Tournament

def main():
	create_tournaments()

def create_tournaments():
	t_names = [
	"league-of-legends-challenger-korea",
	"league-of-legends-challenger-series",
	"league-of-legends-champions-korea",
	"league-of-legends-china-lspl",
	"league-of-legends-circuito-brasileiro",
	"league-of-legends-japan-league",
	"league-of-legends-lcs-europe",
	"league-of-legends-lcs-north-america",
	"league-of-legends-lol-master-series",
	"league-of-legends-oceanic-pro-league",
	"league-of-legends-tencent-lol-pro-league"
	]

	for n in t_names:
		t = Tournament.find_tournament(n)
		if t is None:
			t = Tournament(n)
			t.save()
			
main()
