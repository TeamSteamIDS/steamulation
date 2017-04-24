import csv
import time
import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException


def parse(id, newFileName):
    lang_es = webdriver.ChromeOptions()
    lang_es.add_argument("--lang=en")
    driver = webdriver.Chrome("chromedriver.exe",chrome_options=lang_es)

    #scrolling
    reviewUrl = "http://steamcommunity.com/app/" + id + "/reviews/?browsefilter=toprated&snr=1_5_reviews_"
    driver.get(reviewUrl)
    time.sleep(1)
    curParse = 0
    count = 0

    originSoup = BeautifulSoup(driver.page_source,'html.parser')

    curParse = len(originSoup.findAll("div", { "class" : "date_posted" }))
    click = False
    end = False
    startTime = time.clock()
    while True:
        if driver.current_url != reviewUrl:
            driver.close()
            return 0
            break
        oldSource = driver.page_source
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #after scroll
        newSource = driver.page_source

        if len(newSource) != len(oldSource):
            startTime = time.clock()

        looptime = time.clock() - startTime
        if looptime > 15 and click == False:
            print("finding click")
            try:
                driver.find_element_by_link_text('See More Content').click()
                print("click!!")
                startTime = time.clock()
                continue
            except:
                click = True
                continue

        if looptime > 20 and click == True:
            print("finding end")
            try:
                driver.find_element_by_link_text('share a screenshot, make a video, or start a new discussion!')
                break
            except:
                click = False
                startTime = time.clock()
                end = True
                continue
        if end == True:
            break

    page_source = newSource
    driver.close()

    #parsing
    print("parse "+id)
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
        contentData.append(each.get_text())

    for each in positive:
        if(each.get_text()=="Recommended"):
            positiveData.append(1)
        else:
            positiveData.append(0)

    for each in hour:
        hourData.append(each.get_text())

    for each in helpful:
        helpfulData.append(each.get_text())

    print("write: "+id)
    with open(newFileName, 'w', encoding='utf-8') as f:
    	writer = csv.writer(f)
    	writer.writerow(["user name","positive or negative","total playing time","number of helpful","content"])
    	leng = len(userData)
    	for i in range(leng):
            try:
                writer.writerow([userData[i],positiveData[i],hourData[i],helpfulData[i],contentData[i]])
            except:
                print("out of range")
    f.close()
    print("end: "+id)

tag = sys.argv[1]
#start = sys.argv[2]
count = 0
appIdFile = "../appId/"+"appId_"+tag+".csv"

for id in open(appIdFile):
    for char in id:
        if char in "\n":
            id = id.replace(char,'')
    fileName = tag + "/"+id+".csv"
    newFileName =tag+"/"+"new_"+id+".csv"
    '''
    if os.path.isfile(fileName):
        print(id+" exist!")
    else:
        print(id+" start")
        parse(id)
    '''

    if os.path.isfile(newFileName):
        print(newFileName+' exist')
        continue
    else:
        with open(newFileName, 'w') as fout:
            print('{0} start'.format(newFileName))
        fout.close()
        parse(id, newFileName)
