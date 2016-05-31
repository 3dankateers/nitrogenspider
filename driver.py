import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Driver:
	driver = None 

	@staticmethod
	def get_instance():
		if Driver.driver == None:
			Driver.driver = webdriver.Chrome()
		return Driver.driver
	
	@staticmethod
	def login():
		driver = Driver.get_instance()
		driver.get("https://nitrogensports.eu")
		##assert "Python" in driver.title
		##login_button = driver.find_element_by_id("modal-welcome")
		try:
			login_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "modal-welcome-new-button")))
			print "Logged in"
		except:
			print "login button not found"
		Driver.wait_until(login_button.is_enabled, 5)
		try:
			##time.sleep(5)
			login_button.click()
		except:
			print "Error clicking login"
	
	@staticmethod
	def logout():
		driver = Driver.get_nstance()
		driver.close()
	
	@staticmethod
	def wait_until(somepredicate, timeout, period=0.25):
		mustend = time.time() + timeout
		while time.time() < mustend:
			if somepredicate:
				return True
			time.sleep(period)
		return False