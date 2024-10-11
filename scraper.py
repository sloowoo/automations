from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.service import Service


#put your own here
username = "111"
password = "222"

website = 'https://accounts.veracross.com/williston/portals/login'


#uncomment this part and comment driver=webdriver.Chrome()
#to hide chrome window

# op = webdriver.ChromeOptions()
# op.add_argument("--headless=new")
# #for now, the headless window option makes a blank window pop up
# #the temp solution is to just move the window far off screen
# #fix has already been merged but may not be implemented until later vers
# #https://stackoverflow.com/questions/78996364/chrome-129-headless-shows-blank-window
# op.add_argument("--window-position=-2400,-2400")
# driver = webdriver.Chrome(options=op)

#to see physical chrome window
driver = webdriver.Chrome()
                          
# driver = webdriver.Chrome()
driver.get(website)

#input username
driver.find_element(By.ID, 'username').send_keys(username + Keys.RETURN)
#input password
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'passwd'))).send_keys(password + Keys.RETURN)
#click yes to the microsoft thing
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'idSIButton9'))).send_keys(Keys.RETURN)
#go to student portal
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[@href="'+ "/williston/student/student/overview" +'"]'))).click()


#text formatter
def strip(text):
    return "\n".join([ll.rstrip() for ll in text.splitlines() if ll.strip()])

#assignment scraping function
def assignment_scrape():
    rough_course_links = []
    course_links = []

    #gets all of your courses links and puts them in an array
    links = driver.find_elements(By.XPATH, "//a[@href]")
    for link in links:
        if ('course' in link.get_attribute("href")):
            rough_course_links.append(link.get_attribute("href"))

    #gets rid of link repeats
    course_links = list(set(rough_course_links))
    for page in course_links:
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
                print("CLASS:" + strip(course.text))

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
                    
                date = source.find("div", {"class":"assignment-due-date"})
                rough4 = "due date: " + date.text
                upcoming_date = strip(rough4) + "\n"

                #glue all that text
                upcoming = upcoming_type + upcoming_date + upcoming_summary + upcoming_details
                print(upcoming+'\n' + '----')

                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'close'))).click()
                time.sleep(0.05)

#scrape portal page event
def scrape_events():
    driver.get("https://portals.veracross.com/williston/student")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'event-link')))
    portal = BeautifulSoup(driver.page_source, features="html.parser")
    today =  portal.find("div", {"class":"day today"})
    today_events = today.find_all("a", {"class":"event-link"})
    for event in today_events:
        #don't print out assignments in calendar
        try: 
            if "assignment" in event['href']:
                continue
        except:
            pass
        print(event.text)
                

#scrape_events()        
# assignment_scrape()  


while(True):
    pass
