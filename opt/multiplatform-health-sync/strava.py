#!/usr/bin/python3
"""
    strava.com
"""
import os
import sys

import webbrowser
import json
import requests

import config

def write_to_strava(user_weight):
    # write to strava
    strava_access_token = strava_refresh(json.load(open(config.strava_cfg))) if os.path.isfile(config.strava_cfg) else strava_authenticate()
    strava_user_info = get_strava_user_info(strava_access_token)
    set_strava_user_weight( strava_access_token, float(user_weight), strava_user_info['id']  )   ## For Strava the user weight must be of type float

def strava_authenticate():
    '''if len(sys.argv) > 1:
        paramdata = {
            'client_id': config.strava_athlete_id,
            'client_secret': config.strava_client_secret,
            'code': sys.argv[1],
            'grant_type': 'authorization_code'
        }
        res = requests.post( url = '%s/token' % config.strava_url, data = paramdata)
        out = res.json()
        if res.status_code == 200:
            json.dump(out, open(config.strava_cfg,'w'))
            return out['access_token']
        else:
            print('authentication failed:')
            print(out)
            exit()
    else:'''
    print("No token found, webbrowser will open, authorize the application and copy paste the code section")
    url ='%s/authorize?client_id=%s&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:write,read' % ( config.strava_url, config.strava_athlete_id)
    print(url)
    webbrowser.open(url,new=2)
    strava_code = input("Insert the code fromthe URL after authorizing: ")
    paramdata = {
        'client_id': config.strava_athlete_id,
        'client_secret': config.strava_client_secret,
        'code': strava_code,
        'grant_type': 'authorization_code'
    }
    res = requests.post( url = '%s/token' % config.strava_url, data = paramdata)
    out = res.json()
    if res.status_code == 200:
        json.dump(out, open(config.strava_cfg,'w'))
        return out['access_token']
    else:
        print('authentication failed:')
        print(out)
        exit()

def strava_refresh(data):
    url = '%s/token' % config.strava_url
    res = requests.post(url, params = {
        'client_id': config.strava_athlete_id, 
        'client_secret': config.strava_client_secret,
        'action': 'requesttoken', 
        'grant_type': 'refresh_token',
        'refresh_token': data['refresh_token'],
    })
    out = res.json()
    if res.status_code == 200:
        json.dump(out, open(config.strava_cfg,'w'))
        return out['access_token']
    else:
        print(out)
        exit()

def get_strava_user_info( token):
    url = '%s/athlete' % config.strava_api
    headers = {'Authorization': 'Bearer %s' % token}
    res = requests.get( url, headers=headers)
    if res.status_code != 200:
        print("There was an error reading from Strava API:")
        print( res.json())
    else:
        print("Succesful reading from Strava API")
        return res.json()

def set_strava_user_weight( token, weight, user_id):
    url = '%s/athlete' % config.strava_api
    headers = {'Authorization': 'Bearer %s' % token}
    data = { 'weight': weight, 'id':user_id}
    ## data = {'user[weight]':'%s' % weight}
    res = requests.put( url, headers=headers, data=data)
    if res.status_code != 200:
        print("There was an error writing to Strava API:")
        print( res.json())
    else:
        print("Succesful writing weight to Strava API")
