import bokeh.palettes
import pandas as pd
from bokeh.io import output_file
from bokeh.models import ColumnDataSource, CDSView, GroupFilter
from bokeh.plotting import figure, show
from GMsourcelist import *

dols_apps1920 = pd.read_csv('https://files.digital.nhs.uk/C4/E7282D/dols-eng-applications-2019-20.csv')
dols_demog1920 = pd.read_csv('https://files.digital.nhs.uk/6E/61DF79/dols-eng-demographics-2019-20.csv')
dols_apps1819 = pd.read_csv('https://files.digital.nhs.uk/48/A83A6A/dols-eng-applications-2018-19.csv')
dols_apps1819 = pd.read_csv('https://files.digital.nhs.uk/66/69D8BC/dols-eng-demographics-2018-19.csv')

