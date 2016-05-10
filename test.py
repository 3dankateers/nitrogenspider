import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def scrape():
	global driver
	driver.get("https://nitrogensports.eu/sport/esports/league-of-legends-mid-season-invitational")
	league_events = get_events()

	if league_events != None:
		print league_events
		print str(len(league_events))

def get_events():
	global driver
	try:
		league_events = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "event")))
		return league_events
	except:
		print "no events found"

def parse_events(e):
	try:
		e.


def pause():
	time.sleep(10)


def run():
	login()
	scrape()
	pause()	

run()

