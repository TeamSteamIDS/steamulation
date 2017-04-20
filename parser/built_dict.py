import pickle

import csv

genre = ['Action', 'Adventure', 'Racing', 'RPG', 'Simulation', 'Sports', 'Strategy']
i = 0
for name in genre:
	path = 'parse/appId/appId_' + name
	with open(path, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		for row in spamreader:
			print(row)
	i = i + 1
	if i == 1:
		break