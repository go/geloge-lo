import urllib2
import logging
from urllib import quote, urlencode
from hmac import new as hmac
from hashlib import sha1
from urllib import urlopen

def apicall(host, path, response_type, param):
    ret = None
    url = build_api_url(host, path, response_type, param)
    
    try:
        resp = urllib2.urlopen(url)
        ret = resp.read()
    except (urllib2.HTTPError, urllib2.URLError), error:
        logging.info( str(type(error)) + "error at " + url)
        logging.info(error)

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
    
def api_get(url, params, key):
    params['oauth_signature'] = get_sign('GET', url, params, key)
    request_url = url + '?' + urlencode(params)
    return urlopen(request_url).read()
        
def api_post(url, params, key):
    params['oauth_signature'] = get_sign('POST', url, params, key)
    request_url = url
    return urlopen(request_url, urlencode(params)).read()
    
