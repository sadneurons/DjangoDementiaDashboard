import requests
import pandas as pd
from GMsourcelist import *
import json

drugs = pd.read_csv('GM_antidementia_drugs.csv')
print(drugs.columns)
drugs.columns = ['UNNAMED','TOTAL', 'PRACTICE', 'CCG', 'DRUGCODE',
                 'YEARMONTH', 'DRUGFORM']
print(drugs.columns)
