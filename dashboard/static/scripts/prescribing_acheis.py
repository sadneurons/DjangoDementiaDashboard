import requests
import pandas as pd
from GMsourcelist import *
import json

def getTimeCodes(startmonth="01", startyear="2014",
                 endmonth="12", endyear="2020"):
    # returns a list of codes for the sql query
    returnList=[]
    for year in range(int(startyear), int(endyear)+1):
        for month in range (int(startmonth), int(endmonth)+1):
            if month < 10:
                returnList.append(f"{year}0{month}")
            else:
                returnList.append(f"{year}{month}")
    return returnList



def queryLocalityDrugTime(bnfcode, pcocode, timecode):
    bnfcode = f"'{bnfcode}'"
    print(bnfcode)
    pcocode = f"'{pcocode}'"
    print(pcocode)
    timecode = f"`EPD_{timecode}`"
    print(timecode)
    sql = f"SELECT PCO_NAME, PRACTICE_NAME, YEAR_MONTH, " \
          f"BNF_DESCRIPTION, CHEMICAL_SUBSTANCE_BNF_DESCR, " \
          f"TOTAL_QUANTITY from {timecode} WHERE PCO_CODE={pcocode} AND " \
          f"BNF_CHEMICAL_SUBSTANCE={bnfcode}"
    print(sql)
    formatted_query = sql.replace(" ", "%20")
    print(formatted_query)
    base_url = "https://opendata.nhsbsa.net/api/3/action/datastore_search_sql?sql="
    sql_query= base_url + formatted_query
    print(sql_query)
    returned = requests.get(sql_query)
    df = pd.DataFrame(json.loads(returned.text)['result']['result']['records'])
    return df

def queryGMDrugs(bnfcodes, pcocodes, timecodes):
    list_of_all_dfs=[]
    for bnfcode in bnfcodes:
        for pcocode in pcocodes:
            for timecode in timecodes:
                df = queryLocalityDrugTime(bnfcode, pcocode, timecode)
                list_of_all_dfs.append(df)
    return pd.concat(list_of_all_dfs)



gm_df = queryGMDrugs(bnfcodes = drug_codes.values(), # Donepezil
                     pcocodes = org_codes_sql.values(),
                     timecodes = getTimeCodes())
print(gm_df)
gm_df.to_csv("GM_antidementia_drugs.csv")
