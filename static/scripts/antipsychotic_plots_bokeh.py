import bokeh.palettes
import pandas as pd
from bokeh.io import output_file
from bokeh.models import ColumnDataSource, CDSView, GroupFilter
from bokeh.plotting import figure, show

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
apdata = pd.concat([apdata, apdata2, apdata3])
apdata.CCG = [ccg[4:-4] for ccg in apdata.CCG]
apdata = apdata.groupby(['DATE', 'CCG'], as_index=False).aggregate({'COUNT': ['sum']})
apdata.columns = apdata.columns.get_level_values(0)
apdata.to_csv("./antipsychotic_data_gm.csv")

output_file('bokeh_antipsychotics.html',
            title="Antipsychotics Interactive Figure")
ccglist = list(set(apdata.CCG))
datelist = list(set(apdata.DATE))
colorlist = bokeh.palettes.Spectral10

fig = figure(  # text_align="center",

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
    # x_range=datelist,
    y_axis_label='Count of people',
    y_axis_type='linear',
    y_axis_location='left',
    y_range=(0, 1800),
    title='Dementia antipsychotic prescribing for Greater Manchester CCGs (click labels to hide CCG)',
    title_location='above',
    toolbar_location='right'
    # legend_padding= 10,
    # legend_spacing= 3
)

# Remove the gridlines from the figure() object
fig.grid.grid_line_color = '#FFFFFF'

data = dict(dates=sorted(list(set(apdata.DATE))))
for ccg in ccglist:
    data[ccg] = list(apdata.COUNT[apdata.CCG == ccg])
# pprint(data)
source = ColumnDataSource(data)
# print(grouped)
# print(source)
fig.vbar_stack(ccglist, x='dates', source=data, width=25 * 86400000,
               color=colorlist, legend_label=ccglist)
fig.legend.location = "top_right"
fig.legend.click_policy = "hide"
fig.legend.label_text_font_size = "9pt"
fig.legend.orientation = "horizontal"
fig.legend.glyph_width = 7
fig.legend.glyph_height = 18
fig.title.align = "center"
show(fig)
