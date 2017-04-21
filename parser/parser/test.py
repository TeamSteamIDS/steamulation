import csv
import time
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd


genereList = list()
genere = {'Action': 18, 'Adventure': 8, 'Racing': 0, 'RPG': 3, 'Simulation': 3, 'Sports': 0, 'Strategy': 8}
genereList.append(genere)
genereList.append(genere)
genereList.append(genere)
genereList.append(genere)

fileName = "strategy/"+str(6400)+".csv"

outFile = "racing/"+'test'+".csv"

with open(fileName, 'r') as fin, open(outFile, 'w') as fout:
    writer = csv.writer(fout)
    writer.writerow(["user name","positive or negative","total playing time","number of helpful","content","Action","Adventure","Racing","RPG","Simulation","Sports","Strategy"])
    reader = csv.reader(fin, delimiter=',')
    next(reader, None)
    count = 0
    for row in reader:
        if(len(row)!=0):
            genere = genereList[count]
            count = count + 1
            writer.writerow([row[0],row[1],row[2],row[3],row[4],genere['Action'],genere['Adventure'],genere['Racing'],genere['RPG'],genere['Simulation'],genere['Sports'],genere['Strategy']])

fin.close()
fout.close()
