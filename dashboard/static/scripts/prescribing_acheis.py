import requests
import pandas as pd
from GMsourcelist import *
import json
import os

def getTimeCodes(startmonth="01", startyear="2014",
                 endmonth="12", endyear="2020"):
    # returns a list of codes for the sql query
    datelist = pd.date_range(f"{startyear}-{startmonth}-01",
                                 f"{endyear}-{endmonth}-01", freq="M")
    returnList = [str(date)[:7].replace("-", "") for date in datelist]
    return returnList

def queryLocalityDrugTime(bnfcodes, pcocodes, timecode):
    drug_codes=[f"'{bnfcode}'" for bnfcode in bnfcodes]
    #print(bnfcode)
    org_codes=[f"'{code}'" for code in pcocodes]
    where_statement_1 = "%20OR%20BNF_CHEMICAL_SUBSTANCE=".join(drug_codes)
    where_statement_2 = "%20OR%20PCO_CODE=".join(org_codes)

    timecode = f"`EPD_{timecode}`"
    #print(timecode)
    sql = f"SELECT PCO_NAME, PRACTICE_NAME, YEAR_MONTH, " \
          f"BNF_DESCRIPTION, CHEMICAL_SUBSTANCE_BNF_DESCR, TOTAL_QUANTITY " \
          f"from {timecode} WHERE (BNF_CHEMICAL_SUBSTANCE={where_statement_1}) AND (PCO_CODE={where_statement_2})"
        #print(sql)
    formatted_query = sql.replace(" ", "%20")
    #print(formatted_query)
    base_url = "https://opendata.nhsbsa.net/api/3/action/datastore_search_sql?sql="
    sql_query= base_url + formatted_query
    print(sql_query)
    returned = requests.get(sql_query)
    parsed = json.loads(returned.text)
    try:
        df = pd.DataFrame(json.loads(returned.text)['result']['result']['records'])
        return df
    except KeyError:
        try:
            csv_location = list(parsed['result']['gc_urls'][0].values())[0]
            df = pd.read_csv(csv_location)
            return df
        except KeyError:
            print(parsed)



# def queryLocalityDrugTime(bnfcode, pcocode, timecode):
#     bnfcode = f"'{bnfcode}'"
#     #print(bnfcode)
#     pcocode = f"'{pcocode}'"
#     #print(pcocode)
#     timecode = f"`EPD_{timecode}`"
#     #print(timecode)
#     sql = f"SELECT PCO_NAME, PRACTICE_NAME, YEAR_MONTH, " \
#           f"BNF_DESCRIPTION, CHEMICAL_SUBSTANCE_BNF_DESCR, " \
#           f"TOTAL_QUANTITY from {timecode} WHERE PCO_CODE={pcocode} AND " \
#           f"BNF_CHEMICAL_SUBSTANCE={bnfcode}"
#     #print(sql)
#     formatted_query = sql.replace(" ", "%20")
#     #print(formatted_query)
#     base_url = "https://opendata.nhsbsa.net/api/3/action/datastore_search_sql?sql="
#     sql_query= base_url + formatted_query
#     #print(sql_query)
#     returned = requests.get(sql_query)
#     df = pd.DataFrame(json.loads(returned.text)['result']['result']['records'])
#     return df

def queryGMDrugs(bnfcodes, pcocodes, timecodes, csv_filename):
    list_of_all_dfs=[]
    for timecode in timecodes:
        print(timecode)
        df = queryLocalityDrugTime(bnfcodes, pcocodes, timecode)
        list_of_all_dfs.append(df)
        print(df)
        df.to_csv(csv_filename, mode='a', index=False,
                  header=not os.path.exists(csv_filename))
    return pd.concat(list_of_all_dfs)



#gm_df = queryGMDrugs(bnfcodes = drug_codes.values(), # Donepezil
#                     pcocodes = org_codes_sql.values(),
#                     timecodes = getTimeCodes())
#print(gm_df)
#gm_df.to_csv("GM_antidementia_drugs.csv")



pre_2017_manc_df = queryGMDrugs(bnfcodes = drug_codes.values(),
                    pcocodes = pre_2017_codes.values(),
                    timecodes = getTimeCodes('01','2014','01','2018'),
                                csv_filename='pre_2017_manc_df.csv')
print(pre_2017_manc_df)
