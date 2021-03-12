import operator
from collections import Counter

import pandas as pd
from bokeh.io import output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral10
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap

from GMsourcelist import *

# download and save
# cqc = pd.read_csv('https://www.cqc.org.uk/search/services/care-homes?location=&latitude=&longitude=&sort=default&la=&distance=15&mode=csv')
# cqc.to_csv('./raw_cqc_data.csv', index=False)
cqc = pd.read_csv('raw_cqc_data.csv')
cqcnw = cqc[cqc['Region'] == "North West"]
cqcgmlist = [item.rstrip().lower() in gm_boroughs for item in cqcnw['Local authority']]
chgm = cqcnw[cqcgmlist]
# print(set(chgm['Local authority']))

provlistgm = Counter(chgm['Provider name'])
# print(provlistgm)
borough_listgm = Counter(chgm['Local authority'])

# print(borough_listgm)
# print(chgm)
chgm.to_csv('./care_homes_gm.csv', index=False)

# dementia_care = chgm[chgm['Specialisms/services']
demlist = ['dementia' in item.rstrip().lower() for item in chgm['Specialisms/services']]
demch = chgm[demlist]
# print(demch)
borough_listgm_dem = Counter(demch['Local authority'])
provlistgm_dem = Counter(demch['Provider name'])
# pprint(borough_listgm_dem)
# pprint(provlistgm_dem)


output_file('./dementia_providers_by_borough.html',
            title="Dementia care/nursing homes by borough")
borough_listgm_dem = dict(sorted(borough_listgm_dem.items(), key=operator.itemgetter(1)))
# print(dict(borough_listgm_dem))
tops = list(borough_listgm_dem.values())
names = list(borough_listgm_dem.keys())
fig = figure(  # text_align="center",

    background_fill_color='lightgray',
    background_fill_alpha=0.5,
    border_fill_color='white',
    border_fill_alpha=0.25,
    plot_height=500,
    plot_width=1000,
    # h_symmetry=True, This parameter has been deprecated
    x_axis_label='Borough',
    x_axis_location='below',
    x_range=names,
    y_axis_label='Count of facilities',
    y_axis_type='linear',
    y_axis_location='left',
    y_range=(0, 60),
    title='Dementia care homes in Greater Manchester boroughs',
    title_location='above',
    toolbar_location='right'
    # legend_padding= 10,
    # legend_spacing= 3
)

# Remove the gridlines from the figure() object
fig.grid.grid_line_color = '#FFFFFF'
source = ColumnDataSource(data=dict(names=names, counts=tops))

# print(grouped)
# print(source)
fig.vbar(x='names', top='counts', width=1,
         source=source, line_color='white',
         fill_color=factor_cmap('names', palette=Spectral10,
                                factors=names))

fig.legend.location = "top_right"
# fig.legend.click_policy = "hide"
# fig.legend.label_text_font_size = "9pt"
fig.legend.orientation = "horizontal"
# fig.legend.glyph_width = 7
# fig.legend.glyph_height = 18
fig.title.align = "center"
fig.title.text_font_size = "16pt"
show(fig)
