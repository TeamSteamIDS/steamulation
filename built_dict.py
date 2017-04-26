import pickle

import csv

def classification():
	classification = {}
	genre = ['action', 'adventure', 'racing', 'rpg', 'simulation', 'sports', 'strategy']
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
	with open("dicts/classification.p", "wb") as f:
		pickle.dump(classification, f)
			
'''
for key in classification:
	for g_id in classification[key]:
		path = ''
		with open(path, "r") as f:
		for line in f:
'''	
	

def review(genre):
	with open("dicts/classification.p", "rb") as f:
		classification = pickle.load(f)
	path = ""
	path_new = ""
	cnt = 0
	for g in genre:
		path = 'parser/parser/' + g + '/'
		for g_id in classification[g]:
			path_new = path + str(g_id) + '.csv'
			#print(path_new)
			with open(path_new, "r") as f:
				for line in f:
					print(line)
					cnt = cnt + 1
					if cnt > 10:
						return


classification()				
l = ["racing", "sports"]
review(l)
