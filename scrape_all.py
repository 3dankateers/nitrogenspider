from tournament import Tournament
from scraper import Scraper

tournaments = Tournament.get_array()
##tournaments = [Tournament.find_tournament("league-of-legends-champions-korea")]
sc = Scraper(tournaments)
sc.run()
