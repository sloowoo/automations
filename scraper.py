from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time


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
#go to student portal
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[@href="'+ "/williston/student/student/overview" +'"]'))).click()

rough_course_links = []

#gets all of your courses links and puts them in an array
links = driver.find_elements(By.XPATH, "//a[@href]")
for link in links:
    if ('course' in link.get_attribute("href")):
        rough_course_links.append(link.get_attribute("href"))

#gets rid of link repeats
course_links = list(set(rough_course_links))

#text formatter
def strip(text):
    return "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])

#assignment scraping function
for page in (course_links):
    #/website is where all the assignments at
    if page.endswith("website"):
        driver.get(page)

        #all the types of assignments
        all_shit =[]
        types = ["Homework", "Quiz", "Test", "Project", "Quest", "Lab", "Participation", "Lab", "Classwork"]

        for type in types:
            all_shit += driver.find_elements(By.XPATH, "//span[text()='" + type + "']")

        main_page = BeautifulSoup(driver.page_source, features="html.parser")

        #finds the name of the course
        course = main_page.find("h1")

        #only print out the name if there are assignments or smth
        if len(all_shit) > 0:
            print("-----------------" + '\n')
            print(course.text)

        #listing out assignments
        for homework in all_shit:
            homework.click()
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'assignment-modal')))

            source = BeautifulSoup(driver.page_source, features="html.parser")
            
            #title of assignment
            title = source.find("div", {"class":"title"})
            rough1 = title.text
            upcoming_type = strip(rough1) + "\n"

            #summary of assignment
            summary = source.find("div", {"class":"assignment-description modal-description"})
            rough2 = "summary: " + summary.text
            upcoming_summary = strip(rough2) + "\n"

            #get details of assignment
            #not every one has this
            try:
                details = source.find("li", {"class":"assignment-notes"})
                rough3 = "details: " + details.text
                upcoming_details = strip(rough3) + "\n"
            except:
                upcoming_details = "no details posted."

            #glue all that text
            upcoming = upcoming_type + upcoming_summary + upcoming_details
            print(upcoming+'\n' + '----')

            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'close'))).click()
            time.sleep(0.05)

while(True):
    pass
