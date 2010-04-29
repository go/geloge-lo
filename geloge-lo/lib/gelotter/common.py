from google.appengine.api import urlfetch
import urllib2
import logging
from urllib import quote, urlencode
from hmac import new as hmac
from hashlib import sha1
from urllib import urlopen
from time import time
from random import getrandbits

consumer_key = 'CQiHbpjvmfsla8KqGHwqw'
consumer_secret = 'ZW8Ctox0sIINW0x9h2AOV0TEVHzH41rKDmxZ0ohlXw'

def apicall(host, path, response_type, param):
    ret = None
    url = build_api_url(host, path, response_type, param)
    
    try:
        resp = urllib2.urlopen(url)
        ret = resp.read()
    except (urllib2.HTTPError, urllib2.URLError), error:
        logging.info( str(type(error)) + "error at " + url)
        logging.info(error)
    except urlfetch.DownloadError, error: 
        logging.info( str(type(error)) + "error at " + url)
        logging.info(error)
        pass

    return ret

def build_api_url(host, path, response_type, param):
    ret = ''.join(['http://', host + path, '.', response_type])
    ret += param_to_str(param)
    return ret
    
    
def param_to_str(param):
    ret_params = []
    for key in param:
        ret_params.append('='.join([key, param[key]]))
    return '?' + '&'.join(ret_params)

def get_sign(method, url, params, key):
    ar = [method, 
          url, 
          '&'.join('%s=%s' % (quote(k, ''), 
                              quote(params[k], '')) for k in sorted(params))]
    ar = map((lambda x: quote(x, '')), ar)
    
    message = '&'.join(ar)
    return hmac(key, 
                message, 
                sha1
                ).digest().encode('base64')[:-1]

def get_oauth_params(params = { }, oauth_token = None):
    ret = {
        'oauth_consumer_key' : consumer_key, 
        'oauth_signature_method' : 'HMAC-SHA1', 
        'oauth_timestamp' : str(int(time())), 
        'oauth_nonce' : str(getrandbits(64)), 
        'oauth_version' : '1.0'
        }
    for k in params.keys():
        ret[k] = params[k]

    if oauth_token:
        ret['oauth_token'] = oauth_token

    return ret

def api_get(url, params, token_secret = None):
    key = consumer_secret + '&'
    if token_secret:
        key += token_secret

    params['oauth_signature'] = get_sign('GET', url, params, key)
    request_url = url + '?' + urlencode(params)
    try:
        return urlopen(request_url).read()
    except urlfetch.DownloadError, e: 
        return None
        
def api_post(url, params, token_secret = None):
    key = consumer_secret + '&'
    if token_secret:
        key += token_secret

    params['oauth_signature'] = get_sign('POST', url, params, key)
    request_url = url
    try:
        return urlopen(request_url, urlencode(params)).read()
    except urlfetch.DownloadError, e: 
        return None
