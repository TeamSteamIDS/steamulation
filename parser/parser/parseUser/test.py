import pickle
import pandas as pd
import csv
import time
import os
import re
import sys

with open("../../../dicts/userDictionary_rpg.p", "rb") as f:
    user = pickle.load(f)
    print(user)
