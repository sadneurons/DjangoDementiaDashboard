import pandas as pd
import plotnine as p9
from GMsourcelist import *

 # Load data from the NHS digital website - No API
apdata = pd.read_csv("https://files.digital.nhs.uk/D4/9D8525/dem-diag-anti-psy-Jan-2021-csv.zip")
apdata2 = pd.read_csv('https://files.digital.nhs.uk/0A/739E11/dem-diag-anti-psy-Mar-2020.zip')
apdata3 = pd.read_csv('https://files.digital.nhs.uk/98/E5B106/dem-diag-anti-psy-mar-2019.zip')

# This following sdata is not loaded because there is a big diference in
# rates across areas - likely a difference in how they are coded
# One could apply a normalisation but it would need scrutiny
# apdata4 = pd.read_csv('https://files.digital.nhs.uk/BC/251967/dem-diag-anti-psy-Mar-2018.csv')
# pick out the GM boroughs
def perc(a, b):
    return 100 * a / b

# this produces a percentage column
def clean_function(apdata, level="practice"):
    apdata = apdata[pd.DataFrame(apdata.COMMISSIONER_ORGANISATION_CODE.tolist()).isin(org_codes.values()).any(1).values]
    apdata['ACH_DATE'] = pd.to_datetime(apdata['ACH_DATE'])
    apdata['Value'] = apdata['Value'].replace("*", "0")
    apdata['Value'] = pd.to_numeric(apdata['Value'])
    apdata = apdata.drop(columns=[])
    apdata_ap = apdata[apdata.Measure == "ANTI_PSY_ALL_AGES"]
    apdata_ap.rename(columns={'Value': 'AP'}, inplace=True)
    apdata_ap = apdata_ap.drop(columns='Measure')
    apdata_demreg = apdata[apdata.Measure == "DEM_REGISTER"]
    apdata_demreg.rename(columns={'Value': 'DEMREG'}, inplace=True)
    apdata_demreg = apdata_demreg.drop(columns='Measure')
    apdata = pd.merge(apdata_ap, apdata_demreg, how="inner")
    apdata = apdata.groupby(['ACH_DATE', 'CCG_NAME'], as_index=False).aggregate({'AP':['sum'], 'DEMREG':['sum']})
    apdata.columns = apdata.columns.get_level_values(0)
    apdata['Perc'] = perc(apdata['AP'], apdata['DEMREG']) # percentage column
    return apdata


# pick out the GM boroughs
apdata = clean_function(apdata)
apdata2 = clean_function(apdata2)
apdata3 = clean_function(apdata3)
apdata3['ACH_DATE'][apdata3['ACH_DATE']=='2018-04-30T00:00:00.000000000'] = pd.to_datetime('2018-08-31T00:00:00.000000000')

# print(apdata)
# apdata3['DATE'][apdata3['DATE']=='2018-04-30T00:00:00.000000000'] = pd.to_datetime('2018-08-31T00:00:00.000000000')
# #plot
apdata = pd.concat([apdata, apdata2, apdata3]) # put them together

# save to csv for later / bokeh pltotting

apdata.to_csv("dashboard/static/csv/antipsychotic_data_gm_percentage.csv")

# Beging the static nineplots plot
ap_plot = (p9.ggplot(data=apdata,
                           mapping=p9.aes(x='ACH_DATE', y='Perc',
                                          #color='CCG_NAME',
                                          group='CCG_NAME'))
                 + p9.geom_bar(stat="identity", position="dodge")
               #  + p9.themes.theme_xkcd()
                 + p9.theme(axis_text_x=p9.element_text(angle=90),
                            title=p9.element_text(size=22, face='bold'))
                 + p9.scale_x_datetime(name="Date of returned data")
                 + p9.ggtitle("GM dementia register antipsychotic rx percentage")
                 + p9.facet_wrap("CCG_NAME"))
ap_filename = "apdata_perc.png"
ap_plot.save(ap_filename, width=12, height=12, dpi=600)

## let's see abouu a Bokeh plot


