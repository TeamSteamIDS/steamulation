import pickle
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
