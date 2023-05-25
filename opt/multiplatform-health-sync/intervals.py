#!/usr/bin/python3
"""
    intervals.icu
"""
import os
import sys

import json
import requests
from requests.auth import HTTPBasicAuth

import config

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def set_wellness(event, date):
    requests.packages.urllib3.disable_warnings()
    res = requests.put('%s/wellness/%s' % (config.intervals_api, event['id']), auth=HTTPBasicAuth('API_KEY',config.intervals_api_key), json=event, verify=False)
    if res.status_code != 200:
        print('[' + f'{bcolors.FAIL} \u26A0 {bcolors.ENDC}]{bcolors.FAIL} upload wellness data failed with status code: {res.status_code} {bcolors.ENDC}')
        print(res.json())
    else:
        print('[ i ] Succesful writing ' + str(date) + ' to intervals.icu')