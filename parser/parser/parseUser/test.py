import pickle
import pandas as pd
import csv
import time
import os
import re
import sys

tag = sys.argv[1]
fileName = '../'+tag+'/finish/userDictionary'

with open(fileName, "rb") as f:
    userKey = pickle.load(f)

print(userKey)
