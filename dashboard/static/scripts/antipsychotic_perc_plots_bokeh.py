import bokeh.palettes
import pandas as pd
from bokeh.io import output_notebook, output_file
from bokeh.models import ColumnDataSource, CDSView, GroupFilter
from bokeh.plotting import figure, show
from bokeh.transform import dodge
from pprint import pprint
from GMsourcelist import *
from bokehutils import facet

apdata = pd.read_csv("https://files.digital.nhs.uk/D4/9D8525/dem-diag-anti-psy-Jan-2021-csv.zip")
apdata2 = pd.read_csv('https://files.digital.nhs.uk/0A/739E11/dem-diag-anti-psy-Mar-2020.zip')
apdata3 = pd.read_csv('https://files.digital.nhs.uk/98/E5B106/dem-diag-anti-psy-mar-2019.zip')
apdata3.loc[apdata3.ACH_DATE == '2018-04-30T00:00:00.000000000'] = pd.to_datetime('2018-08-31T00:00:00.000000000')


# apdata4 = pd.read_csv('https://files.digital.nhs.uk/BC/251967/dem-diag-anti-psy-Mar-2018.csv')
# pick out the GM boroughs
def perc(a, b):
    return 100 * a / b


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
    apdata['Perc'] = perc(apdata['AP'], apdata['DEMREG'])
    return apdata


# pick out the GM boroughs
apdata = clean_function(apdata)
apdata2 = clean_function(apdata2)
apdata3 = clean_function(apdata3)


apdata = pd.concat([apdata, apdata2])

apdata.columns = ['DATE', 'CCG', 'AP', 'DEMREG', 'PERC']
apdata.CCG = [ccg[4:-4] for ccg in apdata.CCG]
apdata.to_csv("./antipsychotic_data_gm_percentage.csv",
              index=False)

output_file("./test.html", title="")
ccglist = list(set(apdata.CCG))
datelist = list(set(apdata.DATE))
colorlist = bokeh.palettes.Spectral10

fig = figure(  # text_align="center",

    background_fill_color='lightgray',
    background_fill_alpha=0.5,
    border_fill_color='white',
    border_fill_alpha=0.25,
    plot_height=500,
    plot_width=2000,
    # h_symmetry=True, This parameter has been deprecated
    x_axis_label='Month',
    x_axis_type='datetime',
    x_axis_location='below',
    # x_range=datelist,
    y_axis_label='Count of people',
    y_axis_type='linear',
    y_axis_location='left',
    y_range=(0, 15),
    title='Dementia antipsychotic prescribing for Greater Manchester CCGs (click labels to hide CCG)',
    title_location='above',
    toolbar_location='right'
    # legend_padding= 10,
    # legend_spacing= 3
)

# Remove the gridlines from the figure() object
fig.grid.grid_line_color = '#FFFFFF'
dates=sorted(list(set(apdata.DATE)))
data = dict(dates=dates)
for ccg in ccglist:
    data[ccg] = list(apdata.PERC[apdata.CCG == ccg])
#pprint(data)
source = ColumnDataSource(data)
# print(grouped)
# print(source)
f=figure()
points(f, 'dates', 'ccg', source=source)
fig=facet_grid(f, 'dates', 'ccg',
               groups="ccg", plot_width=100, plot_height=100,
               share_x_range = True,
               share_y_range = True)
fig.legend.location = "top_right"
fig.legend.click_policy = "hide"
fig.legend.label_text_font_size = "9pt"
fig.legend.orientation = "horizontal"
fig.legend.glyph_width = 7
fig.legend.glyph_height = 18
fig.title.align = "center"
show(fig)
