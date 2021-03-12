import fingertips_py as ftp
from pprint import pprint
from gm_phe_functions import *
from GMsourcelist import *
import pandas as pd
# Download relevant GM PHE data to csv files with appropriate labels
all_inds = ftp.metadata.get_metadata_for_all_indicators()
with open("phe_indicators.csv", 'w+') as  d:
    d.write(all_inds.to_csv())
