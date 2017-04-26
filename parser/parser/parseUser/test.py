import pickle
import pandas as pd
import csv
import time
import os
import re
import sys




#def get_total_review(g_id,u_id):

fileName = '../../../dicts/userDictionary_racing.p'

with open(fileName, "rb") as f:
    review = pickle.load(f)

    print(review)

#total_review = get_total_review()
