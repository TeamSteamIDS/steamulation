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
	review = {}
	total_play = {}
	for g in genre:
		path = 'parser/parser/' + g + '/finish/'
		for g_id in classification[g]:
			path_new = path + str(g_id) + '.csv'
			print(path_new)
			f = open(path_new, 'rt')
			cnt = 0
			try:
				reader = csv.reader(f)
				for l in reader:
					cnt = cnt + 1
					if cnt == 1:
						continue
					rev_id = str(g_id) + str(cnt)
					v = {}
					v['content'] = l[4]
					v['game_id'] = g_id
					# retrieve user_id
					user_list = l[0].split("/")
					#
					v['user_id'] = user_list[len(user_list) - 2]
					v['recommand'] = l[2]
					# retrieve helpful
					help_list = l[4].split(" people ")
					print(l[4],help_list)
					num_help_list = help_list[0].split(" of ")
					num_feel_helpful = num_help_list[0].split("\t")[-1]
					if len(num_help_list) == 1:
						if "No" in num_help_list[0]:
							v['helpful'] = 1.0
						else:
							v['helpful'] = 0.0
					else:
						v['helpful'] = int(num_feel_helpful.replace(',',''))/int(num_help_list[1].replace(',',''))
					#
					tup = (g_id, v['user_id'])
					total_play[tup] = float(l[3].split(" hrs")[0].replace(',',''))
					review[rev_id] = v
			finally:
				f.close()

	with open("dicts/review.p", "wb") as f:
		pickle.dump(review, f)
	
classification()				
l = ["racing"]
review(l)
