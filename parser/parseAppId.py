import csv
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("html/Strategy.html"),'html.parser')

appId = soup.findAll("tr", {"class" : "app"})

app =[]

for each in appId:
    app.append(each.attrs['data-appid'])

with open('appId/appId_Strategy.csv', 'w') as f:
    writer = csv.writer(f)
    for elem in app:

        writer.writerow([elem])
