from cgi import parse_qs
from datetime import datetime

from google.appengine.ext import db
from gelotter.common import api_get, api_post, get_oauth_params

authz_uri = 'http://twitter.com/oauth/authorize'

class Token(db.Model):
    oauth_token = db.StringProperty(required=True)
    oauth_token_secret = db.StringProperty(required=True)
    time_created = db.DateTimeProperty(required=True)
    screen_name = db.StringProperty()
    user_id = db.StringProperty()

def request_token():
    uri = 'http://twitter.com/oauth/request_token'
    params = get_oauth_params()
    res = api_get(uri, params)
    if not res:
        return None

    res_param = parse_qs(res)

    if not res_param.has_key('oauth_token'):
        return None
    if not res_param.has_key('oauth_token_secret'):
        return None

    return Token(
        oauth_token = res_param['oauth_token'][0], 
        oauth_token_secret = res_param['oauth_token_secret'][0], 
        time_created = datetime.now()
        )

def authorize(oauth_token):
    uri = 'http://twitter.com/oauth/access_token'
    params = get_oauth_params(oauth_token = oauth_token)
    res = api_post(uri, params)
    if not res:
        return None

    res_param = parse_qs(res)

    if not res_param.has_key('oauth_token'):
        return None
    if not res_param.has_key('oauth_token_secret'):
        return None
    if not res_param.has_key('screen_name'):
        return None
    if not res_param.has_key('user_id'):
        return None
    
    return Token(
        oauth_token = res_param['oauth_token'][0], 
        oauth_token_secret = res_param['oauth_token_secret'][0], 
        time_created = datetime.now(), 
        screen_name = res_param['screen_name'][0],
        user_id = res_param['user_id'][0]
        )
        
