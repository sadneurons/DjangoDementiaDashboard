import bokeh.palettes
import pandas as pd
from GMsourcelist import *
from bokeh.io import output_file
from bokeh.plotting import figure, show



# get some data from nhs digital website and analyse it for GM
# with a view to creating a dementia dashboard website for GM
data2020 = pd.read_csv(ccg_diagnoses2020)
data2019 = pd.read_csv(ccg_diagnoses2019)
data2018 = pd.read_csv(ccg_diagnoses2018)
data2017 = pd.read_csv(ccg_diagnoses2017)


data=pd.concat([data2020, data2019, data2018, data2017])
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

diagnosis_rates = diagnosis_rates.pivot(index=["NAME",
                                               "ACH_DATE"],
                                        columns="MEASURE",
                                        values="VALUE").reset_index().rename_axis(None, axis=1)
diagnosis_rates.columns = ['CCG', 'DATE', 'RATE', 'LL', 'UL']
diagnosis_rates.CCG = [ccg[4:-4] for ccg in diagnosis_rates.CCG]
diagnosis_rates.to_csv("./diagnosis_rates.csv", index=False)

output_file('bokeh_diagnosis.html',
            title="Empty Bokeh Figure")
#fig = figure()

fig = figure(#text_align="center",

             background_fill_color='lightgray',
             background_fill_alpha=0.5,
             border_fill_color='white',
             border_fill_alpha=0.25,
             plot_height=500,
             plot_width=1000,
             # h_symmetry=True, This parameter has been deprecated
             x_axis_label='Month',
             x_axis_type='datetime',
             x_axis_location='below',
             #x_range=('2018-01-01', '2018-06-30'),
             y_axis_label='Diagnosis rates (% estimated)',
             y_axis_type='linear',
             y_axis_location='left',
             y_range=(60, 100),
             title='Dementia diagnostic rates for Greater Manchester CCGs (click labels to hide CCG)',
             title_location='above',
             toolbar_location='right'
            #legend_padding= 10,
            #legend_spacing= 3
            )

# Remove the gridlines from the figure() object
fig.grid.grid_line_color = '#FFFFFF'

ccglist = list(set(diagnosis_rates.CCG))
colorlist=bokeh.palettes.Spectral10

for item, name in enumerate(ccglist):
    plot_line = diagnosis_rates[diagnosis_rates.CCG == name]
    fig.line(x=plot_line.DATE, y=plot_line.RATE, color=colorlist[item],
             legend_label=name)
    fig.circle(x=plot_line.DATE, y=plot_line.RATE, line_width=0.7, color=colorlist[item],
               legend_label=name)
fig.legend.location = "top_right"
fig.legend.click_policy ="hide"
fig.legend.label_text_font_size = "7pt"
fig.legend.glyph_width = 10
fig.legend.glyph_height = 25
fig.legend.orientation = "horizontal"
fig.title.align="center"
show(fig)

