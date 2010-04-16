import urllib2

api_host = 'twitter.com'
def apicall(path, response_type, uid):
    # TODO error handling
    url = build_api_url(path, response_type, {'id' : uid})
    resp = urllib2.urlopen(url)
    body = resp.read()
    return body

def build_api_url(path, response_type, param):
    ret = ''.join(['http://', api_host + path, '.', response_type])
    ret += param_to_str(param)
    return ret
    
    
def param_to_str(param):
    ret_params = []
    for key in param:
        ret_params.append('='.join([key, param[key]]))
    return '?' + '&'.join(ret_params)










