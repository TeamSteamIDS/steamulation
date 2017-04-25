import csv
import time
import os
import re
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import steamapi

steamapi.core.APIConnection(api_key="56C90FBD8CC1C30B69E55D0194282197")
me = steamapi.user.SteamUser(76561197996416028)

print(me.games)
