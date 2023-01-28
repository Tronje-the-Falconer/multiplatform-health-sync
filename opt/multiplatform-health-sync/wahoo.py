#!/usr/bin/python3
"""
    wahoo.com
"""
import os
import sys
import webbrowser
import requests
import json

import config

def write_to_wahoo(weight):
    # Get Wahoo_access_token or refresh the token
    wahoo_access_token = wahoo_refresh(json.load(open(config.wahoo_cfg))) if os.path.isfile(config.wahoo_cfg) else wahoo_authenticate()
    wahoo_user_info = get_wahoo_user( wahoo_access_token)
    print('Retreived Wahoo userid %s for %s %s' % (wahoo_user_info['id'], wahoo_user_info['first'], wahoo_user_info['last']))
    set_wahoo_user_weight( wahoo_access_token, weight)


def get_wahoo_user( token ):
    url = '%s/v1/user' % config.wahoo_api
    res = requests.get(url, headers={'Authorization': 'Bearer %s' % token})
    return res.json() 

def set_wahoo_user_weight( token, weight):
    url = '%s/v1/user' % config.wahoo_api
    headers = {'Authorization': 'Bearer %s' % token}
    data = {'user[weight]':'%s' % weight}
    res = requests.put( url, headers=headers, data=data)
    if res.status_code != 200:
        print("There was an error writing to Wahoo API:")
        print( res.json())
    else:
        print("Succesful writing weight to Wahoo API")

def wahoo_authenticate():
    print('No token found, webbrowser will open, authorize the application and copy paste the code section')
    url = '%s/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code&scope=%s' % ( config.wahoo_api, config.wahoo_client_id,config.wahoo_redirect_uri,config.wahoo_scopes)
    print(url)
    webbrowser.open(url,new=2)
    wahoo_code = input('Insert the code from the URL after authorizing: ')
    paramdata = {
        'action': 'requesttoken', 
        'code': wahoo_code,
        'client_id': config.wahoo_client_id,
        'client_secret': config.wahoo_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': config.wahoo_redirect_uri
    }
    res = requests.post('%s/oauth/token' % config.wahoo_api, params = paramdata )
    out = res.json()
    if res.status_code == 200:
        json.dump(out, open(config.wahoo_cfg,'w'))
        return out['access_token']
    else:
        print('authentication failed:')
        print(out)
        exit()

def wahoo_refresh(data):
    """refresh current token
    this makes sure we won't have to reauthorize again."""

    url = '%s/oauth/token' % config.wahoo_api
    res = requests.post(url, params = {
        'client_id': config.wahoo_client_id, 'client_secret': config.wahoo_secret,
        'action': 'requesttoken', 'grant_type': 'refresh_token',
        'refresh_token': data['refresh_token'],
    })
    out = res.json()
    if res.status_code == 200:
        json.dump(out, open(config.wahoo_cfg,'w'))
        return out['access_token']
    else:
        print(out)
        exit()