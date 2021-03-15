import pandas as pd
import plotnine as p9

from GMsourcelist import *

apdata = pd.read_csv("https://files.digital.nhs.uk/D4/9D8525/dem-diag-anti-psy-Jan-2021-csv.zip")
apdata2 = pd.read_csv('https://files.digital.nhs.uk/0A/739E11/dem-diag-anti-psy-Mar-2020.zip')
apdata3 = pd.read_csv('https://files.digital.nhs.uk/98/E5B106/dem-diag-anti-psy-mar-2019.zip')


# apdata4 = pd.read_csv('https://files.digital.nhs.uk/BC/251967/dem-diag-anti-psy-Mar-2018.csv')
# pick out the GM boroughs
def clean_function(apdata, level="practice"):
    apdata = apdata[pd.DataFrame(apdata.COMMISSIONER_ORGANISATION_CODE.tolist()).isin(org_codes.values()).any(1).values]
    apdata = apdata[apdata.Measure == "ANTI_PSY_ALL_AGES"]
    apdata['Value'] = apdata['Value'].replace("*", "0")
    apdata['Value'] = pd.to_numeric(apdata['Value'])
    if level == "practice":
        apdata = apdata[['CCG_NAME', "NAME", 'ACH_DATE', 'Value']]
        # need to change the date to actual dates
        ################
        apdata.columns = ['CCG', 'PRACTICE', 'DATE', 'COUNT']
    if level == "ccg":
        apdata = apdata[['CCG_NAME', 'ACH_DATE', 'Value']]
        apdata.columns = ['CCG', 'DATE', 'COUNT']
    # apdata['DATE'] = apdata['DATE'].str[2:5] + " " + \
    # apdata['DATE'].str[5:]
    apdata['DATE'] = pd.to_datetime(apdata['DATE'])
    return (apdata)


# pick out the GM boroughs
apdata = clean_function(apdata)
apdata2 = clean_function(apdata2)
apdata3 = clean_function(apdata3)
# apdata4 = clean_function(apdata4)
# cleanup error in Tameside and Glossop Date


apdata3['DATE'][apdata3['DATE'] == '2018-04-30T00:00:00.000000000'] = \
    pd.to_datetime('2018-08-31T00:00:00.000000000')
# plot
apdata = pd.concat([apdata, apdata2, apdata3])

ap_plot = (p9.ggplot(data=apdata,
                     mapping=p9.aes(x='DATE', y='COUNT',
                                    fill='CCG',
                                    group='CCG'))
           + p9.geom_bar(stat="identity", position="stack")
           + p9.themes.theme_xkcd()
           + p9.theme(axis_text_x=p9.element_text(angle=45),
                      title=p9.element_text(size=22, face='bold'))
           + p9.ggtitle("GM dementia register antipsychotic rx"))
ap_filename = "apdata.png"
ap_plot.save(ap_filename, width=12, height=12, dpi=600)

# <= except it does not have ligatures - well now it DOES!
# What an extraordinary font! IT is both monospaced
# and cursive, with cursive for the comments
# I wonder who actually created it <- some feckin genius!
#
