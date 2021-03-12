import fingertips_py as ftp
from pprint import pprint
from gm_phe_functions import *
from GMsourcelist import *
import pandas as pd
# Download relevant GM PHE data to csv files with appropriate labels
report_groups = ["palliative and end of life care profiles"]
report_sub_groups = ["dementia", "home"]

for group in report_group:
    for subgroup in report_sub_groups:
        item_dict = get_phof_ids(group, subgroup)  # returns a dict
        for key, value in item_dict.items():
        #print(key, str(value))
            download_gm_data(filename=key, code=int(value))
