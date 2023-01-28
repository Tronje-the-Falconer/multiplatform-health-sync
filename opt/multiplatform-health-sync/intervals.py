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


def set_wellness(event, date):
    requests.packages.urllib3.disable_warnings()
    res = requests.put('%s/wellness/%s' % (config.intervals_api, event['id']), auth=HTTPBasicAuth('API_KEY',config.intervals_api_key), json=event, verify=False)
    if res.status_code != 200:
        print('upload wellness data failed with status code:', res.status_code)
        print(res.json())
    else:
        print('Succesful writing ' + str(date) + ' to intervals.icu')