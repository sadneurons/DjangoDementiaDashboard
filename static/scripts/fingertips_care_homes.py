import fingertips_py as ftp
import bokeh.palettes
from GMsourcelist import *
from bokeh.io import output_file
from bokeh.plotting import figure, show
import pandas as pd
from bokeh.palettes import Spectral10

#
# phof = ftp.get_profile_by_name("palliative and end of life care profiles")
# phof_meta = ftp.get_metadata_for_profile_as_dataframe(phof["Id"])
# print(phof_meta.columns)
# careids = ["care" in item.lower() for item in phof_meta.Indicator]
# care_ids = phof_meta['Indicator ID'][careids]
# print(care_ids)
#indicator_meta = phof_indicators[phof_meta["Indicator"].str.contains("Healthy")]
#print(indicator_meta)
care_data = ftp.get_data_for_indicator_at_all_available_geographies(92489)

phe_dict = { 'percentage deaths care homes': 93475,
             "carehome beds per 100 75+": 923489}

#print(care_data['Area Code'])
# return the dat a where the Area Code is in ons_code.values()

row_list = [item in ons_code.values() for item in care_data['Area Code']]
gm_care_data = care_data[row_list]
gm_care_data['Year'] = [pd.to_datetime(str(i)[0:4]) for i in gm_care_data['Time period Sortable']]
gm_care_data = gm_care_data[gm_care_data["Age"] == '75+ yrs']
gm_care_data.sort_values(by="Year", inplace=True)
gm_care_data.to_csv('./care_homes_75.csv')

output_file('Care_home_beds_bokeh.html',
            title="Care home beds per 100 over 75")
#fig = figure()

fig = figure(#text_align="center",

             background_fill_color='lightgray',
             background_fill_alpha=0.5,
             border_fill_color='white',
             border_fill_alpha=0.25,
             plot_height=500,
             plot_width=1000,
             # h_symmetry=True, This parameter has been deprecated
             x_axis_label='Year',
             x_axis_type='datetime',
             x_axis_location='below',
             #x_range=('2018-01-01', '2018-06-30'),
             y_axis_label='Care home beds per 100 people over 75y',
             y_axis_type='linear',
             y_axis_location='left',
             y_range=(6, 16),
             title='Care home beds per 100 people aged 75+ for GM CCGs (click labels to hide CCG)',
             title_location='above',
             toolbar_location='right'
            #legend_padding= 10,
            #legend_spacing= 3
            )

# Remove the gridlines from the figure() object
fig.grid.grid_line_color = '#FFFFFF'

ccglist = list(set(gm_care_data['Area Name']))
colorlist=bokeh.palettes.Spectral10

for item, name in enumerate(ccglist):
    plot_line = gm_care_data[gm_care_data['Area Name'] == name]
    fig.line(x=plot_line['Year'],
             y =plot_line['Count']/(plot_line['Denominator']/100),
             color=colorlist[item],
             legend_label=name)
    fig.circle(x=plot_line['Year'],
               y=plot_line['Count']/(plot_line['Denominator']/100),
               line_width=2,
               color=colorlist[item],
               legend_label=name)
fig.legend.location = "top_right"
fig.legend.click_policy ="hide"
fig.legend.label_text_font_size = "7pt"
fig.legend.glyph_width = 15
fig.legend.glyph_height = 30
fig.legend.orientation = "horizontal"
fig.title.align="center"
fig.title.text_font_size= "14pt"
show(fig)
