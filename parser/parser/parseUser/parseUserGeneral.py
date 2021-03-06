import csv
import time
import os
import re
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import steamapi

def parseUser(fileName, newFileName, csvtag, csvid):

    df = pd.read_csv(fileName)
    username = list()
    recommend = list()
    time = list()
    helpful = list()
    content = list()
    for each in df[df.columns[0]]:
        if each != '':
            username.append(each)
    for each in df[df.columns[1]]:
        if each != '':
            recommend.append(each)
    for each in df[df.columns[2]]:
        if each != '':
            time.append(each)
    for each in df[df.columns[3]]:
        if each != '':
            helpful.append(each)
    for each in df[df.columns[4]]:
        if each != '':
            content.append(each)

    print('UserNum: {0}'.format(len(username)))
    genereList = []
    userLevel = []
    for each in username:
        print(each)
        if each == '':
            continue

        user = each
        generes = {'action':0 ,'adventure':0 ,'racing':0 ,'rpg':0 ,'simulation':0 ,'sports':0 ,'strategy':0}
        appidList = []
        #Regular Expression
        idReg = re.compile('http://steamcommunity.com/id/(.*)/')
        profileReg = re.compile('http://steamcommunity.com/profiles/(.*)/')

        idMatch = re.match(idReg, user)
        profileMatch = re.match(profileReg, user)
        if idMatch:
            name = idMatch.group(1)
            try:
                me = steamapi.user.SteamUser(userurl=name)
                userLevel.append(me.level)
                for each in me.games:
                    appidList.append(each.appid)
            except:
                genereList.append(generes)
                print('exception')
                continue
        elif profileMatch:
            name = profileMatch.group(1)
            try:
                me = steamapi.user.SteamUser(name)
                userLevel.append(me.level)
                for each in me.games:
                    appidList.append(each.appid)
            except:
                genereList.append(generes)
                print('exception')
                continue
        else:
            print('not found user')
            genereList.append(generes)
            continue

        for id in appidList:
            genereTag = ['action','adventure','racing','rpg','simulation','sports','strategy']
            found = 0
            for tag in genereTag:
                if found == 0:
                    fileNameApp = "../../appId/appId_"+ tag  + ".csv"
                    with open(fileNameApp, 'rt') as f:
                        reader = csv.reader(f, delimiter=',')
                        for row in reader:
                            if str(id) == row[0]:
                                generes[tag] = generes[tag] + 1
                                found = 1
                                break

        genereList.append(generes)
        print(generes)
    print(len(genereList))
    outFile = newFileName
    with open(outFile, 'w') as fout:
        writer = csv.writer(fout)
        writer.writerow(["user name","user level","positive or negative","total playing time","number of helpful","content","Action","Adventure","Racing","RPG","Simulation","Sports","Strategy"])
        for i in range(len(username)):
            try:
                genere = genereList[i]
                writer.writerow([username[i],userLevel[i],recommend[i],time[i],helpful[i],content[i],genere['action'],genere['adventure'],genere['racing'],genere['rpg'],genere['simulation'],genere['sports'],genere['strategy']])
            except:
                print('out of index')
    print('{0} succeed'.format(outFile))
    fout.close()

steamapi.core.APIConnection(api_key="56C90FBD8CC1C30B69E55D0194282197")

tag = sys.argv[1]
#start = sys.argv[2]
count = 0
appIdFile = "../../appId/"+"appId_"+tag+".csv"
for id in open(appIdFile):
    for char in id:
        if char in "\n":
            id = id.replace(char,'')
    fileName = "../"+tag+"/parseNew_"+id+".csv"
    newFileName = "../"+tag+"/finish/"+id+".csv"

    if os.path.isfile(fileName):
        if os.path.isfile(newFileName):
            print(newFileName+' exist')
            count = count+1
            continue
        else:
            with open(newFileName, 'w') as fout:
                print('{0} start'.format(newFileName))
            fout.close()

        print(id+" start!")
        userList = []
        df = pd.read_csv(fileName)

        for each in df[df.columns[0]]:
            userList.append(each)
        print(count)
        parseUser(fileName,newFileName, tag, id)
    else:
        print(id+" not exist")
