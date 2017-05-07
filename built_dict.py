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
	result = {}
	game_user = {}#{'action':{}, 'adventure':{}, 'racing':{}, 'rpg':{}, 'simulation':{}, 'sports':{}, 'strategy':{}}
	for g in genre:
		path = 'parser/parser/' + g + '/finish/'
		for g_id in classification[g]:
			path_new = path + str(g_id) + '.csv'
			#print(path_new)
			print(g_id)
			cnt = 0
			try:
				f = open(path_new, 'rt')
				reader = csv.reader(f)
				for l in reader:
					cnt = cnt + 1
					if cnt == 1:
						continue
					rev_id = str(g_id) + str(cnt)
					v = {}
					v['content'] = l[-8]
					v['game_id'] = g_id
					# retrieve user_id
					user_list = l[0].split("/")
					#
					v['user_id'] = user_list[len(user_list) - 2]
					v['recommend'] = l[2]
					if g_id in result:
						result[g_id][v['user_id']] = v['recommend']
					else:
						result[g_id] = {v['user_id']: v['recommend']}
					# retrieve helpful
					help_list = l[4].split(" people ")
					#print(l[4],help_list)
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

					if g_id not in game_user:
						game_user[g_id] = {}
					if v['user_id'] not in game_user[g_id]:
						game_user[g_id][v['user_id']] = \
						{'total_play_time':float(l[3].split(" hrs")[0].replace(',',''))}
					#print(game_user)
					review[rev_id] = v
			except:
				continue
			finally:
				f.close()

	with open("dicts/game_user.p", "wb") as f:
		pickle.dump(game_user, f)
	with open("dicts/result.p", "wb") as f:
		pickle.dump(result, f)
	with open("dicts/review.p", "wb") as f:
		pickle.dump(review, f)

classification()
#l = ["action","adventure","rpg","simulation","sports","strategy","racing"]
l = ["sports"]
review(l)
