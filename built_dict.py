import pickle

import csv

classification = {}
genre = ['Action', 'Adventure', 'Racing', 'RPG', 'Simulation', 'Sports', 'Strategy']
i = 0
for name in genre:
	g_list = []
	path = 'parser/appId/appId_' + name + '.csv'
	i = 1
	with open(path, "r") as f:
		for line in f:
			g_id = int(line)
			g_list.append(g_id)
	classification[name] = g_list			

for key in classification:
	print(len(classification[key]))

with open("dicts/classification.p", "wb") as f:
        pickle.dump(classification, f)