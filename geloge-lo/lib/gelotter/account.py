from gelotter.common import get_oauth_params, api_get, apicall
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
    body = apicall(api_host, '/1/account/rate_limit_status', 'json' , { })
    if body:
        data = json.loads(body)
    return data

def rate_limit_status2(oauth_token, oauth_token_secret):
    params = get_oauth_params(oauth_token = oauth_token)
    url = 'http://api.twitter.com/1/account/rate_limit_status.json'
    return api_get(url, params, oauth_token_secret)
