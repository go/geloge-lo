from time import time
from random import getrandbits
from google.appengine.ext import db
from hashlib import sha1
from hmac import new as hmac
from urllib import quote, urlencode
from urllib import urlopen
from datetime import datetime
from cgi import parse_qs

class RequestToken(db.Model):
    sid = db.StringProperty(required=True)
    oauth_token = db.StringProperty(required=True)
    oauth_token_secret = db.StringProperty(required=True)
    time_created = db.DateTimeProperty()    

def get_request_token(sid, url, consumer_key, consumer_secret):
    params = {
        'oauth_consumer_key' : consumer_key, 
        'oauth_signature_method' : 'HMAC-SHA1', 
        'oauth_timestamp' : str(int(time())), 
        'oauth_nonce' : str(getrandbits(64)),
        'oauth_version' : '1.0'}

    params['oauth_signature'] = get_sign('GET', 
                                         url,
                                         params,
                                         consumer_secret + '&' )
    
    uri = url + '?' + urlencode(params)
    try:
        ret = urlopen(uri)
        res = parse_qs(ret.read())
        if not res.has_key('oauth_token'):
            # TODO logging
            return None
        if not res.has_key('oauth_token_secret'):
            # TODO logging
            return None

        return RequestToken(sid = sid, 
                            oauth_token = res['oauth_token'][0],
                            oauth_token_secret = res['oauth_token_secret'][0], 
                            time_created = datetime.now())
    except IOError, e:
        # TODO logging
        #print e.args
        return None
    
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


        

    
