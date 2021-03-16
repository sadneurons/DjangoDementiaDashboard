from bokeh.palettes import Category20_20
import pandas as pd
from bokeh.io import output_notebook, output_file
from bokeh.plotting import figure, show


drugs = pd.read_csv('GM_antidementia_drugs.csv')
drugs2 = pd.read_csv('pre_2017_manc_df.csv')

drugs2.PCO_NAME = [" ".join(CCG.split(" ")[1:]) for CCG in drugs2.PCO_NAME]

drugs = pd.concat([drugs, drugs2])

drugs.columns = ['UNNAMED','TOTAL', 'PRACTICE', 'CCG', 'DRUGNAME',
                 'YEARMONTH', 'DRUGFORM']
drugsccg = drugs.groupby(['CCG', 'DRUGNAME', 'YEARMONTH'], as_index=False).aggregate({'TOTAL': ['sum']})
drugsccg.columns = drugsccg.columns.get_level_values(0)
drugsccg.DRUGNAME  = [drug.split(" ")[0] for drug in drugsccg.DRUGNAME]
drugsccg.CCG  = [ccg[:-4] for ccg in drugsccg.CCG]
# drugsccg.YEARMONTH  = [item[:-4] for item in drugsccg.YEARMONTH]
drugsccg.YEARMONTH = [str(YEARMONTH)[-2:] +"-"+ str(YEARMONTH)[:-2]  for YEARMONTH in drugsccg.YEARMONTH]
drugsccg.YEARMONTH = pd.to_datetime(drugsccg.YEARMONTH)
print(list(set(drugsccg.DRUGNAME)))


output_file('../bokehplots/bokeh_rivastigmine.html',
            title="Rivastigmine prescribing in GM")
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
             y_axis_label='Prescribed items',
             y_axis_type='linear',
             y_axis_location='left',
             y_range=(60, 15000),
             title='Rivastigmine prescription rates for Greater Manchester CCGs (click labels to hide CCG)',
             title_location='above',
             toolbar_location='right'
            #legend_padding= 10,
            #legend_spacing= 3
            )

# Remove the gridlines from the figure() object
fig.grid.grid_line_color = '#FFFFFF'

colorlist=Category20_20
rivastigamine = drugsccg[drugsccg.DRUGNAME=="Rivastigmine"]
ccglist = list(set(rivastigamine.CCG))

for item, name in enumerate(ccglist):
    plot_line = rivastigamine[rivastigamine.CCG == name]
    print(plot_line)
    fig.line(x=plot_line.YEARMONTH, y=plot_line.TOTAL, color=colorlist[item],
             legend_label=name)
    fig.circle(x=plot_line.YEARMONTH, y=plot_line.TOTAL, line_width=0.7, color=colorlist[item],
               legend_label=name)
fig.legend.location = "top_right"
fig.legend.click_policy ="hide"
fig.legend.label_text_font_size = "7pt"
fig.legend.glyph_width = 10
fig.legend.glyph_height = 25
fig.legend.orientation = "horizontal"
fig.title.align="center"
show(fig)


output_file('../bokehplots/bokeh_Donepezil.html',
            title="Donepezil prescribing in GM")

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
             y_axis_label='Prescribed items',
             y_axis_type='linear',
             y_axis_location='left',
             y_range=(6000, 30000),
             title='Donepezil prescription rates for Greater Manchester CCGs (click labels to hide CCG)',
             title_location='above',
             toolbar_location='right'
            #legend_padding= 10,
            #legend_spacing= 3
            )

# Remove the gridlines from the figure() object
fig.grid.grid_line_color = '#FFFFFF'

colorlist=Category20_20
donepezil = drugsccg[drugsccg.DRUGNAME=="Donepezil"]
ccglist = list(set(donepezil.CCG))

for item, name in enumerate(ccglist):
    plot_line = donepezil[donepezil.CCG == name]
    print(plot_line)
    fig.line(x=plot_line.YEARMONTH, y=plot_line.TOTAL, color=colorlist[item],
             legend_label=name)
    fig.circle(x=plot_line.YEARMONTH, y=plot_line.TOTAL, line_width=0.7, color=colorlist[item],
               legend_label=name)
fig.legend.location = "top_right"
fig.legend.click_policy ="hide"
fig.legend.label_text_font_size = "7pt"
fig.legend.glyph_width = 10
fig.legend.glyph_height = 25
fig.legend.orientation = "horizontal"
fig.title.align="center"
show(fig)






output_file('../bokehplots/bokeh_Memantine.html',
            title="Mementine prescribing in GM")

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
             y_axis_label='Prescribed items',
             y_axis_type='linear',
             y_axis_location='left',
             y_range=(0, 42000),
             title='Memantine prescription rates for Greater Manchester CCGs (click labels to hide CCG)',
             title_location='above',
             toolbar_location='right'
            #legend_padding= 10,
            #legend_spacing= 3
            )

# Remove the gridlines from the figure() object
fig.grid.grid_line_color = '#FFFFFF'

colorlist=Category20_20
memantine = drugsccg[drugsccg.DRUGNAME=="Memantine"]
ccglist = list(set(donepezil.CCG))

for item, name in enumerate(ccglist):
    plot_line = memantine[memantine.CCG == name]
    print(plot_line)
    fig.line(x=plot_line.YEARMONTH, y=plot_line.TOTAL, color=colorlist[item],
             legend_label=name)
    fig.circle(x=plot_line.YEARMONTH, y=plot_line.TOTAL, line_width=0.7, color=colorlist[item],
               legend_label=name)
fig.legend.location = "top_right"
fig.legend.click_policy ="hide"
fig.legend.label_text_font_size = "7pt"
fig.legend.glyph_width = 10
fig.legend.glyph_height = 25
fig.legend.orientation = "horizontal"
fig.title.align="center"
show(fig)





output_file('../bokehplots/bokeh-Galantamine.html',
            title="Galantamine prescribing in GM")

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
             y_axis_label='Prescribed items',
             y_axis_type='linear',
             y_axis_location='left',
             y_range=(0, 10000),
             title='Galantamine prescription rates for Greater Manchester CCGs (click labels to hide CCG)',
             title_location='above',
             toolbar_location='right'
            #legend_padding= 10,
            #legend_spacing= 3
            )

# Remove the gridlines from the figure() object
fig.grid.grid_line_color = '#FFFFFF'

colorlist=Category20_20
galantamine = drugsccg[drugsccg.DRUGNAME=="Galantamine"]
ccglist = list(set(donepezil.CCG))

for item, name in enumerate(ccglist):
    plot_line = galantamine[galantamine.CCG == name]
    print(plot_line)
    fig.line(x=plot_line.YEARMONTH, y=plot_line.TOTAL, color=colorlist[item],
             legend_label=name)
    fig.circle(x=plot_line.YEARMONTH, y=plot_line.TOTAL, line_width=0.7, color=colorlist[item],
               legend_label=name)
fig.legend.location = "top_right"
fig.legend.click_policy ="hide"
fig.legend.label_text_font_size = "7pt"
fig.legend.glyph_width = 10
fig.legend.glyph_height = 25
fig.legend.orientation = "horizontal"
fig.title.align="center"
show(fig)
