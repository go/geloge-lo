import gelotter.common
from gelotter.common import api_get, api_post
from django.utils import simplejson as json
from gelotter.oauth import get_oauth_params

api_host = 'twitter.com'

def user_timeline(uid, since_id = None):
    # TODO json to constant
    param = {'id' : uid}
    if since_id:
        param['since_id'] = since_id

    body = gelotter.common.apicall(api_host, '/statuses/user_timeline', 'json' , param)
    data = None
    if body:
        data = json.loads(body)
    return data

def user_timeline2(user_id, since_id = None, 
                   oauth_token = None, 
                   oauth_token_secret = None):
    params = { 'id':  user_id}
    if since_id:
        params['since_id'] = since_id

    if oauth_token:
        params = get_oauth_params(oauth_token = oauth_token)
    
    url = 'http://twitter.com/statuses/user_timeline.json'
    result = api_get(url, params, oauth_token_secret)
    if not result:
        return None

    ret = json.loads(result)
    return ret
        
def update(status,
           lat = None, 
           lng = None, 
           display_coordinates = 'false',  
           oauth_token = None, 
           oauth_token_secret = None):
    params = get_oauth_params(oauth_token = oauth_token)
    params['status']  = status

    if lat:
        params['lat'] = lat
    if lng:
        params['long'] = lng

    url = 'http://api.twitter.com/1/statuses/update.json'
    result = api_post(url, params, oauth_token_secret)
    if not result:
        return None

    ret = json.loads(result)
    return ret
    
