from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

username = "your username"
password = "your password"

website = 'https://accounts.veracross.com/williston/portals/login'
op = webdriver.ChromeOptions()
op.add_argument('headless')
driver = webdriver.Chrome(options=op)
driver.get(website)

driver.find_element(By.ID, 'username').send_keys(username + Keys.RETURN)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'passwd'))).send_keys(password + Keys.RETURN)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'idSIButton9'))).send_keys(Keys.RETURN)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[@href="'+ "/williston/student/student/upcoming-assignments" +'"]'))).click()
 
soup = BeautifulSoup(driver.page_source, features="html.parser")
for i in soup.find_all("a", class_="title"):
    name = i.text.strip()
    print(name)