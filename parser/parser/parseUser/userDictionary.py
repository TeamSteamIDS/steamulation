#find . -type f -name "parseNew_*" -print0 | xargs -0 -I {} mv {} new   (move to folder)
#find . -type f -name "parseNew_*" | wc -l  (count numbers)
import pickle
import pandas as pd
import csv
import time
import os
import re
import sys

'''
with open("PATH to .p file", "wb") as f:
        pickle.dump(store, f)
'''

fileList = os.listdir("../racing/new")

print(fileList)
