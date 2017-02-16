import time
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tournament import Tournament
from pro_match import ProMatch
from odd import Odd
from driver import Driver
from helper import parse_date, parse_map_number, parse_team_name, parse_ML
	
class EventException(Exception):
	pass

class Scraper:

	##passed in an array of tournaments to scrape for
	def __init__(self, tournaments):
		self.tournaments = tournaments
		self.driver = Driver.get_instance()
		##TODO find better solution than sleep 
		##time.sleep(10)
	
	def run(self):
		Driver.login()
		for t in self.tournaments:
			self.scrape_tournament(t)
		Driver.logout()
		##time.sleep(20)
		##Driver.driver.save_screenshot('screen2.png')
		##print "took screenshot"

	def scrape_tournament(self, tourny):
		print "**********************************************************************************************"
		print "Scraping:" , tourny.name 
		self.driver.get("https://nitrogensports.eu/sport/esports/" + tourny.name)
		league_events= self.get_events()

		if league_events != None:
			for e in league_events:
				self.parse_event(e, tourny.id)
		print "**********************************************************************************************"

	def get_events(self):
		##Driver.get_instance().save_screenshot('./screenshots/screen2.png')
		time.sleep(10)
		##Driver.get_instance().save_screenshot('./screenshots/screen3.png')
		try:
			league_events = WebDriverWait(self.driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "event")))
			##league_events = self.driver.find_element_by_class_name('event')
			print "Found ", str(len(league_events)), " events"
			return league_events
		except:
			print "no events found"


	def parse_event(self, e, t_id):
		try:
			team1_and_map = str(self.get_team(e, team = 0))
			team2_and_map = str(self.get_team(e, team = 1))
			team1_name = parse_team_name(team1_and_map)
			team2_name = parse_team_name(team2_and_map)

			match_date = str(self.get_date(e))
			match_day = str(parse_date(match_date))

			##if doesnt contain map information
			if "map" in team1_and_map:
				map_number = parse_map_number(team1_and_map)
			else:
				map_number = 1
			

			ML_T1 = parse_ML(str(self.get_ml(e, team = 0)))
			ML_T2 = parse_ML(str(self.get_ml(e, team = 1)))
			scrape_date = datetime.datetime.utcnow()
			
			match = ProMatch.find_match(team1_name, team2_name, map_number, match_day, "nitrogen")

			##update status which holds info about whether match is updated using csv/nitrogen/both
			if match.status == None:
				match.status = "nitrogen"
			elif match.status == "csv":
				match.status = "both"
			
			match.tournament_id = t_id
			match.match_date = match_date
			match.save()
			
			##not sure why this is neccesary, weird format from scraping
			if isinstance(ML_T1, (int, long)) and isinstance(ML_T2, (int, long)):
				odd = {"match_id": match.id, "ML_T1" : ML_T1, "ML_T2" : ML_T2, "scrape_date" : scrape_date}	
				match.odds.append(odd)
				match.save()
				print "odd inserted"
			else:
				print "ODD NOT SAVED ML CANNOT BE PARSED, ", ML_T1

		except EventException:
			print "Invalid Event"

	def get_team(self, e, team = 0):
		try:
			teams = WebDriverWait(e, 1).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "event-participant")))
			assert len(teams) == 2, "2 Teams not found"
			return teams[team].text.split("\n")[0]
		except:
			raise EventException("Invalid Event")
			print "event-participant (teams) not found"

	def get_ml(self, e, team = 0):
		try:
			mls = WebDriverWait(e, 1).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "event-odds")))
			assert len(mls) == 2, "2 MLs not found"
			return mls[team].text
		except:
			raise EventException("Invalid Event")
			print "selectboxit-text (MLs) not found"

	def get_date(self, e):
		try:
			date = e.find_element_by_class_name("event-time-text")
			return date.text
		except:
			raise EventException("Invalid Event")

	def print_team(self, e):
		try:
			team = e.find_element_by_class_name("event-participants")
		except:
			raise EventException("Invalid Event")
