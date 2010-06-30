import gelotter.common
from gelotter.common import api_get, api_post
from django.utils import simplejson as json
from gelotter.oauth import get_oauth_params

api_host = 'search.twitter.com'

def hash_timeline(hashname):
    # TODO json to constant
    param = {'q' : hashname}
#    if since_id:
#        param['since_id'] = since_id

    body = gelotter.common.apicall(api_host, '/search', 'json' , param)
    data = None
    if body:
        data = json.loads(body)
    return data

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
    
