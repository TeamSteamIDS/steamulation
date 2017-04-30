import pickle
import pandas as pd
import csv
import time
import os
import re
import sys

userFileName = '../../../dicts/userDictionary_racing.p'
reviewFileName = '../../../dicts/review.p'
gameFileName = '../../../dicts/game_user.p'

with open(userFileName, "rb") as f:
    user = pickle.load(f)
    f.close()
with open(reviewFileName, "rb") as f:
    review = pickle.load(f)
    f.close()
with open(gameFileName, "rb") as f:
    game = pickle.load(f)
    f.close()


def get_total_review_g(g_id):
    count = 0
    for each in review:
        if review[each]['game_id'] == g_id:
            count = count + 1
    #print('{0} : {1} '.format(g_id,count))
    return count


def get_total_review_u(u_id):
    count = 0
    for each in review:
        if review[each]['user_id'] == u_id:
            count = count + 1
    #print('{0} : {1} '.format(u_id,count))
    return count

'''
#total_review for each game_id
total_review_g = {}
for each in review:
    g_id = review[each]['game_id']
    if g_id not in total_review_g:
        total_review_g[g_id] = get_total_review_g(g_id)

with open('../../../dicts/total_review_g.p', "wb") as f:
        pickle.dump(total_review_g, f)
#total_review for each user_id
total_review_u = {}
for each in review:
    u_id = review[each]['user_id']
    if u_id not in total_review_u:
        total_review_u[u_id] = get_total_review_u(u_id)

with open('../../../dicts/total_review_u.p', "wb") as f:
        pickle.dump(total_review_u, f)
'''
for each in game:
    print(each)
