#find . -type f -name "parseNew_*" -print0 | xargs -0 -I {} mv {} new   (move to folder)
#find . -type f -name "parseNew_*" | wc -l  (count numbers)
import pickle
import pandas as pd
import csv
import time
import os
import re
import sys

#Build Genere of user diction
#output will be /genere/finish/genere.p
#python3 userDictionary.py "genere"

tags = ["racing"]
userField = ['userLevel', 'action', 'adventure', 'racing', 'rpg', 'simulation', 'sports', 'strategy']
userKey = {}
for tag in tags:
    fileList = os.listdir("../"+tag+"/finish")
    for fileName in fileList:
        print('{0} start'.format(fileName))
        #try:
        if fileName != '.DS_Store':
            fileName = '../'+tag+'/finish/' + fileName
            df = pd.read_csv(fileName)
            userName = list()
            userLevel = list()
            action = list()
            adventure = list()
            racing = list()
            rpg = list()
            simulation = list()
            sports = list()
            strategy = list()
            for each in df[df.columns[0]]:
                if each != '':
                    userName.append(each)
            for each in df[df.columns[1]]:
                if each != '':
                    userLevel.append(each)
            for each in df[df.columns[6]]:
                if each != '':
                    action.append(each)
            for each in df[df.columns[7]]:
                if each != '':
                    adventure.append(each)
            for each in df[df.columns[8]]:
                if each != '':
                    racing.append(each)
            for each in df[df.columns[9]]:
                if each != '':
                    rpg.append(each)
            for each in df[df.columns[10]]:
                if each != '':
                    simulation.append(each)
            for each in df[df.columns[11]]:
                if each != '':
                    sports.append(each)
            for each in df[df.columns[12]]:
                if each != '':
                    strategy.append(each)

            for i in range(len(userName)):
                userValue = {'userLevel':0, 'action':0, 'adventure':0, 'racing':0, 'rpg':0, 'simulation':0, 'sports':0, 'strategy':0 }
                userValue['userLevel'] = userLevel[i]
                userValue['action'] = action[i]
                userValue['adventure'] = adventure[i]
                userValue['racing'] = racing[i]
                userValue['rpg'] = rpg[i]
                userValue['simulation'] = simulation[i]
                userValue['sports'] = sports[i]
                userValue['strategy'] = strategy[i]
                user_list = userName[i].split("/")
                userKey[user_list[len(user_list) - 2]] = userValue
        #except:
            #print('{0} error'.format(fileName))
            #continue

with open('../../../dicts/userDictionary_all'+'.p', "wb") as f:
    pickle.dump(userKey, f)
