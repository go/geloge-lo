from time import time
from random import getrandbits
from cgi import parse_qs
from datetime import datetime

from google.appengine.ext import db
from gelotter.common import api_get, api_post

class Token(db.Model):
    oauth_token = db.StringProperty(required=True)
    oauth_token_secret = db.StringProperty(required=True)
    time_created = db.DateTimeProperty(required=True)
    screen_name = db.StringProperty()
    user_id = db.StringProperty()

def request_token(oauth_consumer_key, oauth_consumer_secret):
    uri = 'http://twitter.com/oauth/request_token'
    params = { 
        'oauth_consumer_key' : oauth_consumer_key, 
        'oauth_signature_method' : 'HMAC-SHA1', 
        'oauth_timestamp' : str(int(time())), 
        'oauth_nonce' : str(getrandbits(64)), 
        'oauth_version' : '1.0'
        }
    res = api_get(uri, params, oauth_consumer_secret + '&')
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

def authorize(oauth_token, oauth_consumer_key, oauth_consumer_secret):
    uri = 'http://twitter.com/oauth/access_token'
    params = { 
        'oauth_token' : oauth_token, 
        'oauth_consumer_key' : oauth_consumer_key, 
        'oauth_signature_method' : 'HMAC-SHA1', 
        'oauth_timestamp' : str(int(time())), 
        'oauth_nonce' : str(getrandbits(64)), 
        'oauth_version' : '1.0'
        }
    res = api_post(uri, params, oauth_consumer_secret + '&')
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
        
