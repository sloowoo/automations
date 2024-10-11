from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import regex as re


#put your own here
username = "111"
password = "222"

website = 'https://accounts.veracross.com/williston/portals/login'



#to hide chrome window
op = webdriver.ChromeOptions()
op.add_argument("--headless=new")
#for now, the headless window option makes a blank window pop up
#the temp solution is to just move the window far off screen
#fix has already been merged but may not be implemented until later vers
#https://stackoverflow.com/questions/78996364/chrome-129-headless-shows-blank-window
op.add_argument("--window-position=-2400,-2400")
driver = webdriver.Chrome(options=op)

#to see physical chrome window
# driver = webdriver.Chrome()
                          
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
                
                
#prints diff text based on the type of event
def type_match(type, event):
    match type:
        case "WC":
            print("WC: " + event.text[3:10] + event.text[21:])

        case "Reed":
            print("DOD in Reed: " + event.text[3:10] + event.text[23:])
            
        case "REED":
            return
 
        case "LAS":
            print("DOD in LAS: " + event.text[3:10] + event.text[22:])

        case "MRC":
            print("MRC: " + event.text[3:10] + event.text[22:])

        case "SRC":
            print("SRC: " + event.text[3:10] + event.text[22:])
        case _:
            return
                
                

#scrape portal page event
def scrape_events():
    driver.get("https://portals.veracross.com/williston/student")
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'event-link')))
    portal = BeautifulSoup(driver.page_source, features="html.parser")
   
    #find all days in calendar
    day_tags = portal.find_all("div", {"class":"day"})

    for day in day_tags:
    
        date = day.find("div", {"class":"day-header"})
        events = day.find_all("a", {"class":"event-link"})
        
        #skip day if no events
        if len(events) == 0:
            continue
        
        #print dates with blue or green if it says
        if "Blue" in events[0].text or "Green" in events[0].text:
            print('\n' + "-----------------")
            print(date.text + ' ' + events[0].text + '\n')
        else:
            print('\n' + "-----------------")
            print(date.text + '\n')

        #most common types of calendar shit 
        event_types = ["WC", "Reed", "REED", "LAS", "MRC", "SRC"]

        #loop through every event in a day column
        for event in events:
            #dont print if the event is an assignment
            try: 
                if "assignment" in event['href']:
                    continue
            except:
                pass
            
            found_type = False
            #loops through all the most common types of events
            #if not a common type then found_type stays false
            for type in event_types:
                if type in event.text:
                    #if found type print its custom text
                    type_match(type, event)
                    found_type = True
                else:
                    pass
            
            #just prints the event text raw if not a common type
            if not found_type:
                if "Blue" in event.text or "Green" in event.text:
                    pass
                else:
                    print(event.text)
                
                
#scrape_events()        
#assignment_scrape()  

driver.quit()

# while(True):
#     pass
