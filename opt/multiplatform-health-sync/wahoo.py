#!/usr/bin/python3
"""
    wahoo.com
"""




def get_wahoo_user( token ):
    url = '%s/v1/user' % wahoo_api
    res = requests.get(url, headers={'Authorization': 'Bearer %s' % token})
    return res.json() 

def set_wahoo_user_weight( token, weight):
    url = '%s/v1/user' % wahoo_api
    headers = {'Authorization': 'Bearer %s' % token}
    data = {'user[weight]':'%s' % weight}
    res = requests.put( url, headers=headers, data=data)
    if res.status_code != 200:
        print("There was an error writing to Wahoo API:")
        print( res.json())
    else:
        print("Succesful writing weight to Wahoo API")

def wahoo_authenticate():
    '''
    if len(sys.argv) > 1:
        paramdata = {
            'action': 'requesttoken', 
            'code': sys.argv[1],
            'client_id': wahoo_client_id,
            'client_secret': wahoo_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': wahoo_redirect_uri
        }
        res = requests.post('%s/oauth/token' % wahoo_api, params = paramdata )
        out = res.json()
        if res.status_code == 200:
            json.dump(out, open(wahoo_cfg,'w'))
            return out['access_token']
        else:
            print('authentication failed:')
            print(out)
            exit()
    else:
    '''
    print('No token found, webbrowser will open, authorize the application and copy paste the code section')
    url = '%s/oauth/authorize?client_id=%s&redirect_uri=%s&response_type=code&scope=%s' % ( wahoo_api, wahoo_client_id,wahoo_redirect_uri,wahoo_scopes)
    webbrowser.open(url,new=2)
    wahoo_code = input('Insert the code fromthe URL after authorizing: ')
    paramdata = {
        'action': 'requesttoken', 
        'code': wahoo_code,
        'client_id': wahoo_client_id,
        'client_secret': wahoo_secret,
        'grant_type': 'authorization_code',
        'redirect_uri': wahoo_redirect_uri
    }
    res = requests.post('%s/oauth/token' % wahoo_api, params = paramdata )
    out = res.json()
    if res.status_code == 200:
        json.dump(out, open(wahoo_cfg,'w'))
        return out['access_token']
    else:
        print('authentication failed:')
        print(out)
        exit()

def wahoo_refresh(data):
    """refresh current token
    this makes sure we won't have to reauthorize again."""

    url = '%s/oauth/token' % wahoo_api
    res = requests.post(url, params = {
        'client_id': wahoo_client_id, 'client_secret': wahoo_secret,
        'action': 'requesttoken', 'grant_type': 'refresh_token',
        'refresh_token': data['refresh_token'],
    })
    out = res.json()
    if res.status_code == 200:
        json.dump(out, open(wahoo_cfg,'w'))
        return out['access_token']
    else:
        print(out)
        exit()