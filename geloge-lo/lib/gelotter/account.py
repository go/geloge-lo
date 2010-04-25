import gelotter.common
from django.utils import simplejson as json

from time import time
from random import getrandbits
from google.appengine.ext import db
from hashlib import sha1
from hmac import new as hmac
from urllib import quote, urlencode
from urllib import urlopen
from datetime import datetime
from cgi import parse_qs

api_host = 'api.twitter.com'

def rate_limit_status():
    data = None
    body = gelotter.common.apicall(api_host, '/1/account/rate_limit_status', 'json' , { })
    if body:
        data = json.loads(body)
    return data

def get_sign(method, url, params, key):
    ar = [method.upper(), 
          url, 
          '&'.join('%s=%s' % (quote(k, ''), 
                              quote(params[k], '')) for k in sorted(params))]
    ar = map((lambda x: quote(x, '')), ar)
        
    message = '&'.join(ar)
    return hmac(key, 
                message, 
                sha1
                ).digest().encode('base64')[:-1]

def rate_limit_status2(consumer_key, consumer_key_secret, oauth_token, oauth_token_secret):
    params = {
        'oauth_consumer_key' : consumer_key, 
        'oauth_token' : oauth_token, 
        'oauth_signature_method' : 'HMAC-SHA1', 
        'oauth_timestamp' : str(int(time())), 
        'oauth_nonce' : str(getrandbits(64)),
        'oauth_version' : '1.0'}
    url = 'http://api.twitter.com/1/account/rate_limit_status.json'
    params['oauth_signature'] = get_sign('GET', url, params, consumer_key_secret + '&' + oauth_token_secret)
    uri = url + '?' + urlencode(params)
    return urlopen(uri).read()
