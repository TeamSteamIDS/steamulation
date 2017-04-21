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
    for each in userList:
        lang_es = webdriver.ChromeOptions()
        lang_es.add_argument("--lang=en")
        driver = webdriver.Chrome("chromedriver.exe",chrome_options=lang_es)

        userUrl = each #http://steamcommunity.com/id/freddanorsk/
        '''
        driver.get(userUrl)
        time.sleep(1)
        driver.find_element_by_link_text('Games').click()
        time.sleep(1)
        '''
        userGames = userUrl + 'games/?tab=all'
        driver.get(userGames)
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source,'html.parser')
        #driver.close()
        gameList = soup.findAll("div", {"class" : "popup_block2"})

        #count game generes in user
        genereList = list()
        generes = {'Action':0 ,'Adventure':0 ,'Racing':0 ,'RPG':0 ,'Simulation':0 ,'Sports':0 ,'Strategy':0}
        for id in gameList:
            appid = id.attrs['id'].replace('links_dropdown_','')
            gameUrl = 'http://store.steampowered.com/app/' + appid
            #print(gameUrl)
            try:
                driver.get(gameUrl)
            except:
                print("error")
                continue

            #time.sleep(1)
            soup = BeautifulSoup(driver.page_source,'html.parser')
            #driver.close()
            genre = soup.findAll("div", {"class" : "glance_tags popular_tags"})
            for each in genre:
                #soup = BeautifulSoup(each,'html.parser')
                tag = each.get_text()
                for char in tag:
                    if char in '\n' or char in '\t':
                        tag = tag.replace(char,'')

                try:
                    generes[tag] = generes[tag] + 1
                except:
                    print(tag)

            genereList.append(generes)

        with open(fileName, 'r') as fin, open('new_'+fileName, 'w') as fout:
            writer = csv.writer(fout)
            writer.writerow(["user name","positive or negative","total playing time","number of helpful","content",
            "Action","Adventure","Racing","RPG","Simulation","Sports","Strategy"])
            reader = csv.reader(fin, newline='', lineterminator='\n')
            lis=[line.split() for line in fin]        # create a list of lists
            for i,x in enumerate(lis):              #print the list items
                genere = genereLis[i]
                writer.writerow([
                genere['Action'],genere['Adventure'],genere['Racing'],
                genere['RPG'],genere['Simulation'],genere['Sports'],genere['Strategy']])

        fin.close()
        fout.close()

fileName = "strategy/"+str(2720)+".csv"
userList = []

df = pd.read_csv(fileName)

for each in df[df.columns[0]]:
    userList.append(each)

parseUser(userList, fileName)
