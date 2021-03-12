# -*- coding: utf-8 -*-
import pandas as pd
import requests

from GMsourcelist import *


def get_all_cqc_ch_location_codes_in_ccg(borough):
    """Takes an ODS code (3 characters) not an ONS code"""
    borough = borough.lower()
    ods_code = org_codes[borough]
    base_url = "https://api.cqc.org.uk/public/v1/locations"
    request_url = base_url + "?odsCcgCode=" + ods_code
    request_result = requests.get(request_url)
    report_text = request_result.content.decode('utf-8')
    return (report_text)


def save_all_cqc_ch_locations_in_ccg(borough: str) -> int:
    """Takes a borough name adn returns a csv file of
    all of the locations using pandas functions"""
    json_list = get_all_cqc_location_codes_in_ccg(borough)
    filename = borough + ".csv"
    with open(filename, "w") as data_file:
        f = pd.read_json(json_list)
        f.to_csv(filename)
    return 0


def get_all_cqc_ccg_location_codes_in_ccg(borough):
    """Takes an ODS code (3 characters) not an ONS code"""
    borough = borough.lower()
    ods_code = org_codes[borough]
    base_url = "https://api.cqc.org.uk/public/v1/locations"
    request_url = base_url + "?odsCcgCode=" + ods_code
    request_result = requests.get(request_url)
    report_text = request_result.content.decode('utf-8')
    return (report_text)


def get_plaintxt_cqc_report_from_code(report_code: str) -> str:
    base_url = "https://api.cqc.org.uk/public/v1/reports/"
    request_url = base_url + report_code + "?partnerCode=GMDRC"
    request_result = requests.get(request_url, headers={"Accept": "text/plain"})
    report_text = request_result.content.decode('utf-8')
    return (report_text)
