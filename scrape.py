import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from tournament import Tournament
from match import Match
from odd import Odd

from db_client import DbClient

driver = webdriver.Chrome()
def login():
	global driver
	driver.get("https://nitrogensports.eu")
	##assert "Python" in driver.title
	##login_button = driver.find_element_by_id("modal-welcome")
	try:
		login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "modal-welcome-new-button")))
		login_button.click()
		print "Logged in"
	except:
		print "login button not found"

def scrape_tournament():
	global driver
	##TODO generalize this for all tournaments
	##go to specific page for now
	driver.get("https://nitrogensports.eu/sport/esports/league-of-legends-mid-season-invitational")
	##TODO find better solution than sleep 
	time.sleep(5)
	
	name = get_tournament_name()
	print name

	t = Tournament.find_tournament(name)
	t.save()

	league_events= get_events()

	if league_events != None:
		for e in league_events:
			parse_event(e, t.id)

def get_events():
	global driver
	try:
		league_events = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "event")))
		print "Found ", str(len(league_events)), " events"
		return league_events
	except:
		print "no events found"

class EventException(Exception):
	pass

def parse_event(e, t_id):
	try:
		team1 = get_team(e, team = 0)
		team2 = get_team(e, team = 1)
		match_date = str(get_date(e))
		ML_T1 = get_ml(e, team = 0)
		ML_T2 = get_ml(e, team = 1)
		scrape_date = time.time()
		print match_date
		
		match = None
		match = Match.find_match(t_id, team1, team2, match_date)
		match.save()
		odd = Odd(match.id, ML_T1, ML_T2, scrape_date)
		odd.save()

	except EventException:
		print "Invalid Event"

def get_tournament_name():
	global driver
	try:
		page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "page-find-games")))
		title = WebDriverWait(page, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "page-title")))
		return title.text
	except:
		print "wtf"
		raise EventException("Invalid Page(No Title)")

def get_team(e, team = 0):
	try:
		teams = WebDriverWait(e, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "event-participant")))
		assert len(teams) == 2, "2 Teams not found"
		return teams[team].text.split("\n")[0]
	except:
		raise EventException("Invalid Event")
		print "event-participant (teams) not found"

def get_ml(e, team = 0):
	try:
		mls = WebDriverWait(e, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "event-odds")))
		assert len(mls) == 2, "2 MLs not found"
		return mls[team].text
	except:
		raise EventException("Invalid Event")
		print "selectboxit-text (MLs) not found"

def get_date(e):
	try:
		date = e.find_element_by_class_name("event-time-text")
		return date.text
	except:
		raise EventException("Invalid Event")

def print_team(e):
	try:
		team = e.find_element_by_class_name("event-participants")
	except:
		raise EventException("Invalid Event")


def pause():
	time.sleep(10)


def run():
	global driver
	login()
	scrape_tournament()
	driver.close()

run()

