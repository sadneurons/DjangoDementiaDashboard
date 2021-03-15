# -*- coding: utf-8 -*-
import operator
from collections import Counter
from pprint import pprint
import math
import pandas as pd
from bokeh.io import output_file
from bokeh.models import ColumnDataSource
from bokeh.palettes import Inferno
from bokeh.plotting import figure, show
from bokeh.transform import factor_cmap

from GMsourcelist import *

active = pd.read_csv("active_locations.csv")
care_homes = active[active['Care home?'] == "Y"]
care_homes_nw = care_homes[care_homes['Location Region'] == "North West"]

listhomes = care_homes_nw['Location ONSPD CCG'].tolist()
gm_boroughs_rows = [item[4:-4].lower() in gm_boroughs for item in listhomes]
care_homes_gm = care_homes_nw[gm_boroughs_rows]
# pprint(care_homes_gm['Location Name'])
# pprint(care_homes_gm['Care homes beds'])
# pprint(sum(care_homes_gm['Care homes beds']))

beds_by_borough = care_homes_gm.groupby('Location ONSPD CCG', as_index=False)['Care homes beds'].sum()
# pprint(beds_by_borough)
# pprint(locations_by_borough)
# pprint(Counter(care_homes_gm['Location Primary Inspection Category']))

output_file('./care_home_beds_by_borough.html',
            title="Care/nursing home beds by CCG")

beds_by_borough.columns = ['CCG', 'Care home beds']
beds_by_borough.CCG = [item[4:-4] for item in beds_by_borough.CCG]
beds_by_borough = beds_by_borough.sort_values(by="Care home beds")
pprint(beds_by_borough)
tops = list(beds_by_borough['Care home beds'])
names = list(beds_by_borough['CCG'])
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
    y_range=(0, 3000),
    title='Care home beds in Greater Manchester CCG catchments',
    title_location='above',
    toolbar_location='right',
    tools = "pan,wheel_zoom, save, box_zoom,reset,hover"
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
         fill_color=factor_cmap('names', palette=Inferno.get(10),
                                factors=names))

fig.legend.location = "top_right"
# fig.legend.click_policy = "hide"
# fig.legend.label_text_font_size = "9pt"
fig.legend.orientation = "horizontal"
# fig.legend.glyph_width = 7
# fig.legend.glyph_height = 18
fig.title.align = "center"
fig.title.text_font_size = "16pt"
fig.xaxis.major_label_orientation = math.pi/12
show(fig)

locations_by_borough = dict(Counter(care_homes_gm['Location ONSPD CCG']))
locations_by_borough = dict(sorted(locations_by_borough.items(), key=operator.itemgetter(1)))

pprint(locations_by_borough)

tops = list(locations_by_borough.values())
names = [item[4:-4] for item in locations_by_borough.keys()]

output_file('./care_homes_by_borough.html',
            title="Care/nursing homes by CCG")

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
    y_range=(0, 100),
    title='Care homes in Greater Manchester CCG catchments',
    title_location='above',
    toolbar_location='right',
    tools = "pan,wheel_zoom,save,box_zoom,reset,hover,"

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
         fill_color=factor_cmap('names', palette=Inferno.get(10),
                                factors=names))

fig.legend.location = "top_right"
# fig.legend.click_policy = "hide"
# fig.legend.label_text_font_size = "9pt"
fig.legend.orientation = "horizontal"
# fig.legend.glyph_width = 7
# fig.legend.glyph_height = 18
fig.title.align = "center"
fig.title.text_font_size = "16pt"
fig.xaxis.major_label_orientation = math.pi/12
show(fig)
