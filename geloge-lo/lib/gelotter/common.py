import urllib2
import logging

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

