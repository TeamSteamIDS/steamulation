def get_num_games(g_id, u_id):
    target = ""
    for g in classification:
        if g_id in classification[g]:
            target = g
            break
    return user[u_id][target]

def get_avg_user_level(g_id):
    level_total = 0
    cnt = 0
    for u in game_user[g_id]:
        if u in user:
            level_total = level_total + user[u]['userLevel']
            cnt = cnt + 1
    return level_total/cnt

def get_avg_user_playtime(g_id):
    playtime_total = 0
    cnt = 0
    for u in game_user[g_id]:
        playtime_total = playtime_total + game_user[g_id][u]['total_play_time']
        cnt = cnt + 1
    return playtime_total/cnt

def get_avg_user_playtime_in_G(g_id):
    playtime_total = 0
    num_user = 0
    target = ""
    for g in classification:
        if g_id in classification[g]:
            target = g
            break
    for all_other_g in classification[target]:
        if all_other_g not in result:
            continue
        for u in game_user[all_other_g]:
            playtime_total = playtime_total + game_user[all_other_g][u]['total_play_time']
            num_user = num_user + len(game_user[all_other_g])
    return playtime_total/num_user

def get_user_playtime(g_id, u_id):
    return game_user[g_id][u_id]['total_play_time']

def get_user_level(u_id):
    return user[u_id]['userLevel']

#remember to load pickle file: review.p
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


import pickle
<<<<<<< HEAD
import pandas as pd
import csv
import time
import os
import re
import sys

with open("../../../dicts/userDictionary_racing.p", "rb") as f:
    user = pickle.load(f)


#f = open('out.txt', 'w')
#sys.stdout = f
print(user['76561198053775355'])
=======
import random
import numpy as np
with open("dicts/result.p", "rb") as f:
    result = pickle.load(f)
with open("dicts/classification.p", "rb") as f:
    classification = pickle.load(f)
with open("dicts/userDictionary_racing.p", "rb") as f:
    user = pickle.load(f)
with open("dicts/game_user.p", "rb") as f:
    game_user = pickle.load(f)
with open("dicts/review.p", "rb") as f:
    review = pickle.load(f)




cnt = 0
#print(result['4290'])
for key in result:
    if key not in game_user:
        result.pop(key)

for i in result:
    cnt = cnt + len(result[i])
#print(result)
test_size = cnt * 0.2
test = {}
train = {}
while len(test) < test_size:
    g_id, val = random.choice(list(result.items()))
    u_id, res = random.choice(list(val.items()))
    tup = (g_id, u_id)
    if tup not in test:
        test[tup] = res
#print(test)
for g_id in result:
    for u_id in result[g_id]:
        tup = (g_id, u_id)
        #print(tup)
        if tup not in test:
            #print(result[g_id][u_id])
            train[tup] = result[g_id][u_id]

#print(list(game_user.keys()))
len_train = len(train)
N = len_train
X_train = np.zeros((N+1, 8))
Y_train = np.zeros((N+1, 1))
cnt = 0
for key in train:
    #print(key, train[key])
    g_id = key[0]
    u_id = key[1]
    #l = []
    X_train[cnt,0] = get_num_games(g_id, u_id)
    X_train[cnt,1] = get_avg_user_level(g_id)
    X_train[cnt,2] = get_avg_user_playtime(g_id)
    X_train[cnt,3] = get_avg_user_playtime_in_G(g_id)
    X_train[cnt,4] = get_user_playtime(g_id, u_id)
    X_train[cnt,5] = get_user_level(u_id)
    X_train[cnt,6] = get_total_review_g(g_id)
    X_train[cnt,7] = get_total_review_u(u_id)
    Y_train[cnt] = result[g_id][u_id]
    if cnt % 1000 == 0:
        print(cnt, len_train)
    cnt = cnt + 1
    if cnt > N:
        break
#print(X_train)

#len_train = len(train)
X_test = np.zeros(((N/5)+1, 8))
Y_test = np.zeros(((N/5)+1, 1))
cnt = 0
for key in test:
    #print(key, train[key])
    g_id = key[0]
    u_id = key[1]
    #l = []
    if u_id not in user:
        continue
    X_test[cnt,0] = get_num_games(g_id, u_id)
    X_test[cnt,1] = get_avg_user_level(g_id)
    X_test[cnt,2] = get_avg_user_playtime(g_id)
    X_test[cnt,3] = get_avg_user_playtime_in_G(g_id)
    X_test[cnt,4] = get_user_playtime(g_id, u_id)
    X_test[cnt,5] = get_user_level(u_id)
    X_test[cnt,6] = get_total_review_g(g_id)
    X_test[cnt,7] = get_total_review_u(u_id)
    Y_test[cnt] = int(result[g_id][u_id])
    if cnt % 1000 == 0:
        print(cnt, len_train)
    cnt = cnt + 1
    if cnt > N/5:
        break

#N = 4000
#X_small = X_train[1:N,:]
#Y_small = Y_train[1:N,:]
#X_st = X_test[1:N/5,:]
#Y_st = Y_test[1:N/5,:]
import matplotlib
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

from sklearn.svm import SVC
model_S = SVC(kernel="linear", probability = True)
model_R = SVC(kernel="rbf", probability = True)
model_S.fit(X_train, np.ravel(Y_train))
model_R.fit(X_train,np.ravel(Y_train))
print(model_S.score(X_test, np.ravel(Y_test)))
print(model_R.score(X_test, np.ravel(Y_test)))
>>>>>>> master
