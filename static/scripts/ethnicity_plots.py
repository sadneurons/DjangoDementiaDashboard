import pandas as pd
import plotnine as p9
from GMsourcelist import *
# get some data from nhs digital website and analyse it for GM
# with a view to creating a dementia dashboard website for GM
data = pd.read_csv(ethnicity_diagnoses)
# need to change the date to actual dates

# pick out the GM boroughs
data.columns = ['DATE', 'CCG_CODE', 'ONS_CODE', 'CCG', 'ETHNICITY', 'COUNT']
manc_data_ethnicity = data[['DATE', 'CCG_CODE', 'CCG', 'ETHNICITY', 'COUNT']]
manc_data_ethnicity = data[pd.DataFrame(data.CCG_CODE.tolist()).isin(org_codes.values()).any(1).values]

manc_data_ethnicity['DATE'] = manc_data_ethnicity['DATE'].str[2:5] + " " + manc_data_ethnicity['DATE'].str[5:]
manc_data_ethnicity['DATE'] = pd.to_datetime(manc_data_ethnicity['DATE'])

# rename the cols

print(manc_data_ethnicity)

diagnosis_plot = (p9.ggplot(data=manc_data_ethnicity,
                            mapping=p9.aes(y='COUNT',
                                           group="ETHNICITY",
                                           fill='ETHNICITY',
                                           color='ETHNICITY',
                                           x="DATE"))
                  + p9.geom_bar(stat="identity", size=1)
                  + p9.theme(axis_text_x=p9.element_text(angle=45),
                             title=p9.element_text(size=22, face='bold'))
                  + p9.ggtitle("GM CCG dementia diagnoses by ethnicity")
                  + p9.facet_wrap("CCG"))
diagnosis_plot.save("diagnosis_ethcity.png", width=12, height=12, dpi=600)
