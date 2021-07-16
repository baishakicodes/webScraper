#importing the necessary libraries to help us with the automation
#NOTE: for this to work, you need to have istalled selenium and chromedriver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
import time
import os

#importing dotenv so python can read the credentials for the ccny campus groups in the .env file 
from dotenv import load_dotenv   #for python-dotenv method
load_dotenv()                    #for python-dotenv method

UN = os.environ.get('USER_CCNY')
PW = os.environ.get('PASSWORD_CCNY')

#Change the PATH variable to the directory where your chromedriver is
PATH = "/path/to/your/chromedriver"
login_URL = "URL to the login page"
request_URL = "URL of the page that is your target and behind the login screen"


#initializing the web browser. And getting the login page.
driver = webdriver.Chrome(PATH) 
driver.get(login_URL)

#logging in to the account
username = driver.find_element(By.ID, "SSOUN1")
password = driver.find_element(By.ID, "SSOPWD1")
submit = driver.find_element(By.XPATH,"//button[text()='Sign On']")

#Replace 'username' and 'password' with your username and password respectively
username.send_keys(UN)
password.send_keys(PW)
submit.click()

#waiting for the main page to load
time.sleep(2)

#Clicking the menu to show the directory button
link = driver.find_element(By.ID,'button-menu-mobile')
link.click()

#clicking on the directory button to load the directory page
directory = driver.find_element(By.XPATH,"//a[@href='/people']")
directory.click()
link.click()

#waiting to load the directory page
time.sleep(10)

#finding all undergrad students
unG = driver.find_elements(By.XPATH,'//*[@class="col-md-3 col-padding--10 "]/div/div/div[1]/div[2]/h4/a')

#Change the variable num to the number of emails you want to collect
#Right now i have set it to collect only 1000 emails
#DO NOT change any other variables
num = 200
index = 0
count = 0
name = ""

#This is the main part of the program. This where it loops through
#the names of the students and clicks on each individual student to get their email
#Then it prints the email out to the console
while (count<num):
    #finding all the students graduating 2022
    unG = driver.find_elements(By.XPATH,'//*[@class="col-md-3 col-padding--10 "]/div/div/div[1]/div[2]/h4/a')
    flag  = False
    for i in range(index,len(unG)):
        count = count + 1
        name = unG[i].text
        student = driver.find_element_by_link_text(name)
        try:
            if(flag):
                prevName = unG[i-1].text
                prevStudent = driver.find_element_by_link_text(prevName)
                prevStudent.click()
                time.sleep(2)
                email = driver.find_element(By.XPATH,'//*[@id="primary-modal"]/div/div/div[1]/div/div[2]/div[4]/ul/li[1]/b/a')
                address = email.get_attribute("href")
                eAddress = address[7:]
                print(eAddress)
                x_button = driver.find_element(By.XPATH, '//*[@id="primary-modal"]/div/div/div/div[1]/button')
                x_button.click()
                flag = False
            student.click()
            time.sleep(2)
            email = driver.find_element(By.XPATH,'//*[@id="primary-modal"]/div/div/div[1]/div/div[2]/div[4]/ul/li[1]/b/a')
            address = email.get_attribute("href")
            eAddress = address[7:]
            print(eAddress)
            x_button = driver.find_element(By.XPATH, '//*[@id="primary-modal"]/div/div/div/div[1]/button')
            x_button.click()
        #This is where I check for errors. Most of these errors happen because
        #something doesn't load fast enough and it's trying to click on it when
        #it hasn't load it yet.
        #I tried to respond to these errors as gracefully as possible but there's always
        #something that I might not have caught.
        #Just be as patient as possible!
        except ElementNotInteractableException:
            flag = True
            driver.execute_script("arguments[0].scrollIntoView()", student)
            time.sleep(0.5)
        except:
            try: 
                x_button = driver.find_element(By.XPATH, '//*[@id="primary-modal"]/div/div/div/div[1]/button')
                x_button.click()
                print("something went wrong") 
            except ElementNotInteractableException:
                driver.execute_script("arguments[0].scrollIntoView()", x_button)
                time.sleep(0.5)
                x_button.click()
    index = len(unG)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

time.sleep(2)
driver.close()
