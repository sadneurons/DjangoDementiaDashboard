import pandas as pd
import plotnine as p9
import numpy as np
from GMsourcelist import *
import seaborn as sns

# get some data from nhs digital website and analyse it for GM
# with a view to creating a dementia dashboard website for GM
data = pd.read_csv(ccg_diagnoses)
# need to change the date to actual dates
data['ACH_DATE'] = data['ACH_DATE'].str[2:5] + " " + data['ACH_DATE'].str[5:]
data['ACH_DATE'] = pd.to_datetime(data['ACH_DATE'])
# pick out the GM boroughs
manc_data = data[pd.DataFrame(data.ORG_CODE.tolist()).isin(org_codes.values()).any(1).values]
manc_data = manc_data[['NAME', 'ACH_DATE', 'MEASURE', 'VALUE']]
# rename the cols
diagnosis_rates = manc_data[manc_data['MEASURE'].str.contains('DIAG')]
register = manc_data[manc_data['MEASURE'].str.contains('REGISTER')]
estimates = manc_data[manc_data['MEASURE'].str.contains('ESTIMATE')]
# print(manc_data)
# print(diagnosis_rates)
register.columns = ['CCG', 'DATE', 'MEASURE', 'NUMBER']
register_plot = (p9.ggplot(data=register,
                           mapping=p9.aes(y='NUMBER',
                                          x='DATE',
                                          color="CCG",
                                          group="CCG"))
                 + p9.geom_point(stat="identity", size=4)
                 + p9.geom_line(size=2)
                 + p9.theme(axis_text_x=p9.element_text(angle=45),
                            title=p9.element_text(size=22, face='bold'))
                 + p9.ggtitle("GM CCG dementia registers"))
register_filename = "register_data.png"
register_plot.save(register_filename, width=12, height=12, dpi=600)

diagnosis_rates = diagnosis_rates.pivot(index=["NAME",
                                               "ACH_DATE"],
                                        columns="MEASURE",
                                        values="VALUE").reset_index().rename_axis(None, axis=1)
diagnosis_rates.columns = ['CCG', 'DATE', 'RATE', 'LL', 'UL']
diagnosis_plot = (p9.ggplot(data=diagnosis_rates,
                            mapping=p9.aes(y='RATE',
                                           group="CCG",
                                           color='CCG',
                                           x="DATE"))
                  + p9.geom_line(stat="identity", size=2)
                  + p9.theme(axis_text_x=p9.element_text(angle=45),
                             title=p9.element_text(size=22, face='bold'))
                  + p9.ggtitle("GM CCG dementia diagnosis rates (estimated)"))
diagnosis_plot.save("diagnosis_data.png", width=12, height=12, dpi=600)


