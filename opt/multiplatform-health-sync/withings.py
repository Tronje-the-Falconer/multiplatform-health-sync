#!/usr/bin/python3
"""
    withings.com
"""
import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
import time

import config

def readvalues(delta, token):
    # authorize or refresh
    access_token = refresh(json.load(open(config.withings_cfg))) if os.path.isfile(config.withings_cfg) else authenticate(token)
    
    wellness_delta = {}
    current_day = datetime.fromtimestamp(time.time()).date()
    data = get_measurements(access_token, delta)

    for group in data['measuregrps']:

        # initialize event to push to wellness data
        day = datetime.fromtimestamp(group['date']).date()
        if day not in wellness_delta: wellness_delta[day] = {}

        # iterate over measurements
        for m in group['measures']:
            # fields as defined above
            if m['type'] == 1: wellness_delta[day]['weight'] = float(m['value'] * (10 ** m['unit']))         # weight in kg
            if m['type'] == 6: wellness_delta[day]['bodyfat'] = float(m['value'] * (10 ** m['unit']))       # body fat in %
            if m['type'] == 9: wellness_delta[day]['diastolic'] = float(m['value'] * (10 ** m['unit']))   # in mmHg
            if m['type'] == 10: wellness_delta[day]['systolic'] = float(m['value'] * (10 ** m['unit']))    # in mmHg
            if m['type'] in [71,73]: wellness_delta[day]['temperature'] = float(m['value'] * (10 ** m['unit']))       # in celsius
            # the withings temperature thingy normally would be the source for that, but for what it does it's a bit too pricy for me
            # if someone has one or wants me to have one ;) I can look into this further and adjust this script accordingly.
            
    for day, data in sorted(wellness_delta.items()):
            data['id'] = day.strftime('%Y-%m-%d')
            if data['id'] == current_day.strftime('%Y-%m-%d'):
                values_current_day = data
    
    if not 'values_current_day' in vars():
        print ('no data for today!')
        values_current_day = {}
        
    return wellness_delta, values_current_day

def authenticate(token):
    if token != None:
        res = requests.post('%s/oauth2' % config.withings_api, params = {
            'action': 'requesttoken', 'code': token,
            'client_id': config.withings_client_id, 'client_secret': config.withings_client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': config.withings_redirect_uri,
        })
        out = res.json()
        if out['status'] == 0:
            json.dump(out['body'], open(config.withings_cfg,'w'))
            return out['body']['access_token']
        else:
            print('authentication failed:')
            print(out)
            exit()
    else:
        print('click the link below, authenticate and start this tool again with the code (you should see that in the url) as parameter')
        print('https://account.withings.com/oauth2_user/authorize2?response_type=code&client_id=%s&state=intervals&scope=user.metrics&redirect_uri=%s' % (config.withings_client_id, config.withings_redirect_uri))
        exit()

def refresh(data):
    """refresh current token
    this makes sure we won't have to reauthorize again."""

    url = '%s/oauth2' % config.withings_api
    res = requests.post(url, params = {
        'client_id': config.withings_client_id, 'client_secret': config.withings_client_secret,
        'action': 'requesttoken', 'grant_type': 'refresh_token',
        'refresh_token': data['refresh_token'],
    })
    out = res.json()
    if out['status'] == 0:
        json.dump(out['body'], open(config.withings_cfg,'w'))
        return out['body']['access_token']
    else:
        print(out)
        exit()

def get_measurements(token, delta=0):
    start = datetime.today().date() - timedelta(delta)          # last 8 days
    #start = datetime(2022,1,1)                             # override to initially get all values
    
    url = '%s/measure' % config.withings_api
    res = requests.get(url, headers={'Authorization': 'Bearer %s' % token}, params = {
        'action': 'getmeas', 'meastypes': '1,6,9,10,71,73',
        'category': 1, 'lastupdate': start.strftime('%s'),
    })
    return res.json()['body']