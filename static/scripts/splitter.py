import pandas as pd
from collections import Counter
import re

drugs = pd.read_csv('GM_antidementia_drugs.csv')
drugs2 = pd.read_csv('pre_2017_manc_df.csv')

drugs2.PCO_NAME = [" ".join(CCG.split(" ")[1:]) for CCG in drugs2.PCO_NAME]

drugs = pd.concat([drugs, drugs2])
linelists = [line.split(" ") for line in drugs.BNF_DESCRIPTION]

def starts_with_digit(x):
    return x[0].isdigit()



# y = linelists[4]
# print(y)

doses=[]
for list in linelists:
    doses.append([string for string in list if(starts_with_digit(string))])

drugname=[]
for list in linelists:
    drugname.append(list[0])


# print(doses)
# print(drugname)
print(len(doses))
print(len(drugname))

#drugframe = pd.DataFrame(drugname, doses)

lengths = [len(dose) for dose in doses]
print(set(lengths))
