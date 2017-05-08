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
l = ["racing"]
review(l)


from textblob import TextBlob
from scipy.stats import zscore
def get_review_pos_score(r_id):
    pattern = TextBlob(review[r_id]['content'])
    pol = pattern.sentiment[0]
    sub = pattern.sentiment[1]
    return (pol, sub)

'''
u_review = key: user_id, value: list of review_id of this user
'''

with open("dicts/review.p", "rb") as f:
	review = pickle.load(f)
	u_review = {}
	for each in review:
	    u_id = review[each]['user_id']
	    if u_id in u_review:
	        u_review[u_id].append(each)
	    else:
	        u_review[u_id] = [each]
	with open("dicts/user_review.p", "wb") as f:
	    pickle.dump(u_review, f)

'''
function to generate feature
'''
def get_review_normalized(g_id, u_id):
    list_of_review = u_review[u_id]
    p = []
    s = []
    target = []
    if len(list_of_review) <= 1:
        return (0,0)
    for i in range(len(list_of_review)):
        r_id = list_of_review[i]
        tup = get_review_pos_score(r_id)
        p.append(tup[0])
        s.append(tup[1])
        if g_id == review[r_id]['game_id']:
            target.append(i)
    #print('total review = ', len(list_of_review))
    #print('target len = ', len(target))
    if len(target) == 0:
        return (0,0)
    if np.std(p) == 0:
        a = 0
    else:
        #print(p)
        zp = zscore(p)
        val_p = [zp[x] for x in target]
        a = np.mean(val_p)

    if np.std(s) == 0:
        b = 0
    else:
        #print(s)
        zs = zscore(s)
        val_s = [zs[x] for x in target]
        b = np.mean(val_s)
    return (a, b)


def get_review_helpful(g_id, u_id):
    list_of_review = []
    for r_id in review:
        if review[r_id]['game_id'] == g_id:
            list_of_review.append(r_id)
    sl = []
    target = []
    for i in range(len(list_of_review)):
        r_id = list_of_review[i]
        score = review[r_id]['helpful']
        sl.append(score)
        if u_id == review[r_id]['user_id']:
            target.append(i)
    #print('total review = ', len(list_of_review))
    #print('target len = ', len(target))
    if len(target) == 0:
        return 0
    if np.std(sl) == 0:
        return 0
    else:
        z = zscore(sl)
        val = [z[x] for x in target]
        return np.mean(val)
