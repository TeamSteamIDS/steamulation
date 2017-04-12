import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def parse(id):
    lang_es = webdriver.ChromeOptions()
    lang_es.add_argument("-lang=es")
    lang_es.add_argument("--kiosk")
    driver = webdriver.Chrome(chrome_options=lang_es)
    driver = webdriver.Chrome("chromedriver.exe")
    driver2 = webdriver.Chrome(chrome_options=lang_es)
    driver2 = webdriver.Chrome("chromedriver.exe")
    number=0
    #get total number of reviews
    storeUrl = "http://store.steampowered.com/agecheck/app/" + id
    driver2.get(storeUrl)
    time.sleep(1)
    soup = BeautifulSoup(driver2.page_source,'html.parser')

    try:
        #driver2.find_element_by_link_text('					Enter				').click()
        driver2.find_element_by_link_text('Continue').click()
        print("older than 18")
        time.sleep(1)
    except:
        try:
            driver2.find_element_by_link_text('					Enter				').click()
            #driver2.find_element_by_link_text('Continue').click()
            print("older than 18")
            time.sleep(1)
        except:
            print("nothing")

    for filter in soup.findAll("div",{"class" : "user_reviews_filter_section"}):
    	type = filter.find("label",{"for" : "review_language_mine"})
    	if type:
    		number = type.find("span",{"class" : "user_reviews_count"}).get_text()
    		for char in number:
    			if char in "(,)":
    				number = number.replace(char,'')

    print("number of reviews", number)
    driver2.close()

    #scrolling
    reviewUrl = "http://steamcommunity.com/app/" + id + "/reviews/?browsefilter=toprated&snr=1_5_reviews_"
    driver.get(reviewUrl)
    time.sleep(1)
    curParse = 0
    count = 0

    originSoup = BeautifulSoup(driver.page_source,'html.parser')

    curParse = len(originSoup.findAll("div", { "class" : "date_posted" }))

    while True:
        oldSource = driver.page_source
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #after scroll
        newSource = driver.page_source
        count += 1
        print(count)
        if newSource != oldSource:
            count = 0
        if count > 50:
            try:
                driver.find_element_by_link_text('See More Content').click()
                print("click!!")
                count = 0
            except:
                print("not found click!")
        if count > 100:
            break

    page_source = newSource
    driver.close()

    #parsing
    soup = BeautifulSoup(page_source,'html.parser')
    user = soup.findAll("div", {"class" : "apphub_CardContentAuthorBlock tall"})
    date = soup.findAll("div", { "class" : "date_posted" })
    hour = soup.findAll("div", { "class" : "hours" })
    helpful = soup.findAll("div", { "class" : "found_helpful" })
    positive = soup.findAll("div", { "class" : "title" })
    content = soup.findAll("div", { "class" : "apphub_CardTextContent" })

    userData = []
    userName = []
    dateData = []
    contentData =[]
    positiveData =[]
    hourData = []
    helpfulData = []
    notHelpfulData = []
    funnyData = []
    for each in user:
        userData.append(each.find('a')['href'])

    for each in date:
        dateData.append(each.get_text())

    for each in content:
        contentData.append(each.get_text()[15:])

    for each in positive:
        if(each.get_text()=="Recommended"):
            positiveData.append(1)
        else:
            positiveData.append(0)

    for each in hour:
        hourData.append(each.get_text()[0:4])

    for each in helpful:
        helpfulData.append(each.get_text())

    fileName = id+".csv"
    with open(fileName, 'w') as f:
    	writer = csv.writer(f)
    	writer.writerow(["user name","positive or negative","total playing time","number of helpful","content"])
    	leng = len(userData)
    	for i in range(leng):
    		writer.writerow([userData[i],positiveData[i],hourData[i],helpfulData[i],contentData[i]])

for id in open("appId/appId_Action.csv"):
    parse(str(id))
