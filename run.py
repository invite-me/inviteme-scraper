from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

import os, time

# usernameStr = os.environ.get('EMAIL')
# passwordStr = os.environ.get("PASSWORD")


def read_file(filename="users.txt"):
	with open(filename, "r") as f:
		tmp = f.read()
		tmp = tmp.split("\n")
		return tmp

def write_file(data, filename="out.txt"):
	tmp = "firstname;lastname;email\n"
	for elem in data:
		x = elem.rsplit(" ")
		fname = x[0]
		lname = x[-1]
		tmp+= f"{fname};{lname};{data.get(elem)}\n"

	with open(filename, "w+") as f:
		f.write(tmp)

		return True
with open("config.json", "r") as f:
	a = json.loads(f)
		

	usernameStr = a.get("username")
	passwordStr = a.get("password")
	email_domain = a.get("domain")


users = read_file()
out = dict()


from selenium.webdriver.chrome.options import Options
options = Options()
options.add_argument("user-data-dir=/tmp/tarun")
options.add_experimental_option("detach", True)


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=options)
action = webdriver.ActionChains(driver)

# driver.get("https://teams.microsoft.com/")
driver.get("https://teams.microsoft.com/_#/")

# check if login page appeared
try:
	is_login = driver.find_element(By.ID, 'i0116')
except:
	is_login = False

if is_login:
	# ++++++++++++++++++++++++++++++++++++++++++++++++=

	# Email input field
	username = WebDriverWait(driver, 40).until(
	    EC.element_to_be_clickable(
	        (By.ID, 'i0116')
	    )
	)
	# username = driver.find_element(By.ID, 'i0116')


	# print(username.send_keys(usernameStr))
	username.send_keys(usernameStr)
	time.sleep(3)

	# Click the next button
	# print("click on button")
	# driver.find_element(By.ID, 'idSIButton9').click()
	WebDriverWait(driver, 40).until(
	    EC.element_to_be_clickable(
	        (By.ID, 'idSIButton9')
	    )
	).click()
	# print("button clicked")
	# time.sleep(5)
	#Input field for password
	password = WebDriverWait(driver, 40).until(
	    EC.element_to_be_clickable(
	        (By.ID, 'i0118')
	    )
	)
	# password = driver.find_element(By.ID, 'i0118')
	password.send_keys(passwordStr)
	# time.sleep(5)
	# print("click on button")
	# button = driver.find_element(By.ID, 'idSIButton9')
	# print(button)
	# button.click()
	WebDriverWait(driver, 40).until(
	    EC.element_to_be_clickable (
	        (By.ID, 'idSIButton9')
	    )
	).click()
	# print("button clicked")
	time.sleep(3)
	# driver.find_element(By.ID, 'idSubmit_ProofUp_Redirect').click()
	WebDriverWait(driver, 40).until(
	    EC.element_to_be_clickable(
	        (By.ID, 'idSubmit_ProofUp_Redirect')
	    )
	).click()
	# time.sleep(5)
	# driver.find_element(By.ID, 'CancelLinkButton').click()
	WebDriverWait(driver, 40).until(
	    EC.element_to_be_clickable(
	        (By.ID, 'CancelLinkButton')
	    )
	).click()
	# driver.find_element(By.ID, 'idSIButton9').click()
	WebDriverWait(driver, 40).until(
	    EC.element_to_be_clickable(
	        (By.ID, 'idSIButton9')
	    )
	).click()

	time.sleep(10)
	WebDriverWait(driver, 60).until(
	    EC.element_to_be_clickable(
	        (By.ID, 'app-bar-86fcd49b-61a2-4701-b771-54728cd291fb')
	    )
	).click()

	# driver.find_element(By.ID, 'app-bar-86fcd49b-61a2-4701-b771-54728cd291fb').click()
	# time.sleep(5)
	# driver.send_keys(Keys.chord(Keys.ALT + Keys.N))

	# ++++++++++++++++++++++++++++++++++++++++++++++++=


time.sleep(5)
driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ALT + 'n')


driver.switch_to.frame(driver.find_element(By.CSS_SELECTOR, '[class="embedded-electron-webview embedded-page-content"]'))



for elem in users:
	# inp = driver.find_element(By.ID, "people-picker-input")
	inp = WebDriverWait(driver, 30).until(
		EC.element_to_be_clickable(
			(By.ID, "people-picker-input")
		)
	)
	
	inp.send_keys(elem)
	time.sleep(5)

	# idd = driver.find_element(By.ID, 'downshift-0-menu')
	idd = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable(
			(By.ID, 'downshift-0-menu')
		)
	)

	# user = idd.find_element(By.TAG_NAME, "li")
	user = WebDriverWait(idd, 10).until(
		EC.element_to_be_clickable(
			(By.TAG_NAME, "li")
		)
	)


	x = user.get_attribute('aria-label')
	if not x is None:
		x = user.get_attribute('aria-label').split(",")
		x[-1] = x[-1].replace(" ", "")
		out[x[0]] = f"{x[-1]}{email_domain}"
	else:
		out[elem] = f"===ERROR_NOT_FOUND==="


	WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable(
			(By.ID, "people-picker-input")
		)
	).clear()	

	for i in range(len(inp.get_attribute("value"))):
		inp.send_keys(Keys.BACKSPACE)



for elem in out:
	print(f"{elem} --> {out[elem]} ")

write_file(data=out)