from GMsourcelist import *
import pandas as pd
import fingertips_py as ftp


def get_phof_ids(groupname, idname):
    phof = ftp.get_profile_by_name(groupname)
    phof_meta = ftp.get_metadata_for_profile_as_dataframe(phof["Id"])
    #print(phof_meta.Indicator)
    idnames_matching = [idname in item.lower() for item in phof_meta.Indicator]
    ids = list(phof_meta['Indicator ID'][idnames_matching])
    names = list(phof_meta['Indicator'][idnames_matching])
    return_dict = {names[i]: ids[i] for i in range(len(names))}
    return(return_dict)

def download_gm_data(code: int, filename: str, byFactor="Year"):
    data_frame = ftp.get_data_for_indicator_at_all_available_geographies(code) # use fingertips to download the data
    row_list = [item in ons_code.values() for item in data_frame['Area Code']] # create an index of select only GM rows
    gm_data = data_frame[row_list] # use the row list to sort only GM rows
    gm_data['Year'] = [pd.to_datetime(str(i)[0:4]) for i in gm_data['Time period Sortable']]
    gm_data.sort_values(by=byFactor, inplace=True)
    save_filename = "./" + filename + ".csv"
    gm_data.to_csv(save_filename, index=False)
    return 0
