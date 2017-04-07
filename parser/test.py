import csv
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


soup = BeautifulSoup(open("t.txt"),'html.parser')

#parsing
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
    contentData.append(each.get_text()[20:])

for each in positive:
    if(each.get_text()=="Recommended"):
        positiveData.append(1)
    else:
        positiveData.append(0)

for each in hour:
    hourData.append(each.get_text()[0:4])

for each in helpful:
    helpfulData.append(each.get_text())


with open('test.csv', 'w') as f:
	writer = csv.writer(f)
	writer.writerow(["user name","positive or negative","total playing time","number of helpful","content"])
	leng = len(userData)
	for i in range(leng):
		writer.writerow([userData[i],positiveData[i],hourData[i],helpfulData[i],contentData[i]])

print(len(userData))
