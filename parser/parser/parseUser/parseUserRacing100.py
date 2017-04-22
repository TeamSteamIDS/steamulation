import csv
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


def parseUser(userList,fileName):
    df = pd.read_csv(fileName)
    username = list()
    recommend = list()
    time = list()
    helpful = list()
    content = list()
    for each in df[df.columns[0]]:
        username.append(each)
    for each in df[df.columns[1]]:
        recommend.append(each)
    for each in df[df.columns[2]]:
        time.append(each)
    for each in df[df.columns[3]]:
        helpful.append(each)
    for each in df[df.columns[4]]:
        content.append(each)

    #print('userNum={0}'.format(len(userList)))
    genereList = list()
    userLevel = list()
    for each in userList:
        print(each)
        lang_es = webdriver.ChromeOptions()
        lang_es.add_argument("--lang=en")
        driver = webdriver.Chrome()

        userUrl = each #http://steamcommunity.com/id/freddanorsk/
        userGames = userUrl + 'games/?tab=all'

        #time.sleep(1)
        driver.get(userUrl)


        #level.append()
        try:
            level = driver.find_element_by_xpath("//span[@class='friendPlayerLevelNum']")
            userLevel.append(level.text)
        except:
            userLevel.append(0)

        driver.get(userGames)

        soup = BeautifulSoup(driver.page_source,'html.parser')
        #driver.close()
        gameList = soup.findAll("div", {"class" : "popup_block2"})

        #count game generes in user
        generes = {'Action':0 ,'Adventure':0 ,'Racing':0 ,'RPG':0 ,'Simulation':0 ,'Sports':0 ,'Strategy':0}
        for id in gameList:
            appid = id.attrs['id'].replace('links_dropdown_','')
            gameUrl = 'http://store.steampowered.com/app/' + appid
            genereTag = ['Action','Adventure','Racing','RPG','Simulation','Sports','Strategy']

            #parse generes user has
            for tag in genereTag:
                fileNameApp = "../../../appId/appId_"+ tag  + ".csv"
                with open(fileNameApp, 'rt') as f:
                    reader = csv.reader(f, delimiter=',')
                    for row in reader:
                        if appid == row[0]: # if the username shall be on column 3 (-> index 2)
                            try:
                                generes[tag] = generes[tag] + 1
                                continue
                            except:
                                pass
        genereList.append(generes)
        driver.close()

    outFile = "racing/"+'test'+".csv"
    with open(outFile, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(["user name","user level","positive or negative","total playing time","number of helpful","content","Action","Adventure","Racing","RPG","Simulation","Sports","Strategy"])
        count = 0
        for i in range(len(genereList)):
            genere = genereList[i]
            writer.writerow([username[i],userLevel[i],recommend[i],time[i],helpful[i],content[i],genere['Action'],genere['Adventure'],genere['Racing'],genere['RPG'],genere['Simulation'],genere['Sports'],genere['Strategy']])

    fout.close()
count = 0
for id in open("../../../appId/appId_Racing.csv"):
    count = count + 1
    if count >= 100 abd count <150:
        for char in id:
            if char in "\n":
                id = id.replace(char,'')

        fileName = "../../racing/"+id+".csv"
        if os.path.isfile(fileName):
            print(id+" start!")
            userList = []
            df = pd.read_csv(fileName)
            for each in df[df.columns[0]]:
                userList.append(each)

            parseUser(userList, fileName)
        else:
            print(id+" not exist")
