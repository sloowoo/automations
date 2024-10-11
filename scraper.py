from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

#put your own here
username = "111"
password = "222"

website = 'https://accounts.veracross.com/williston/portals/login'

'''
replacing driver = webdriver.Chrome with the following lines will make it
so that the chrome window will not physically pop up when executing

op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.ChromeOptions(options=op)

'''

driver = webdriver.Chrome()
driver.get(website)

#input username
driver.find_element(By.ID, 'username').send_keys(username + Keys.RETURN)
#input password
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'passwd'))).send_keys(password + Keys.RETURN)
#click yes to the microsoft thing
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'idSIButton9'))).send_keys(Keys.RETURN)

'''
if you want to access main student portal:

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[@href="'+ "/williston/student/student/overview" +'"]'))).click()

'''

class_link = "https://classes.veracross.com/williston/course/"
course_links = []

#gets all of your courses links and puts them in an array
links = driver.find_elements(By.XPATH, "//a[@href]")
for link in links:
    if ('course' in link.get_attribute("href")):
        course_links.append(link.get_attribute("href"))

#everything below this line is experimental so far, will comment later

driver.get('https://classes.veracross.com/williston/course/9198/website')
WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Homework']"))).click()


try:
    WebDriverWait(driver, 20).until(
      EC.presence_of_element_located((By.CLASS_NAME, 'assignment-notes'))
    )
    print(driver.page_source)
except Exception:
    print("fuck")



while(True):
    pass
