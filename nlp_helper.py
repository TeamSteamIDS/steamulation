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