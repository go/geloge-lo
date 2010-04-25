from time import time
from random import getrandbits
from google.appengine.ext import db
from hashlib import sha1
from hmac import new as hmac
from urllib import quote, urlencode
from urllib import urlopen
from datetime import datetime
from cgi import parse_qs

class AccessToken(db.Model):
    sid = db.StringProperty(required=True)
    oauth_token = db.StringProperty(required=True)
    oauth_token_secret = db.StringProperty(required=True)
    time_created = db.DateTimeProperty()    
    screen_name = db.StringProperty(required=True)
    user_id = db.StringProperty(required=True)

def get_access_token(sid, url, oauth_token, consumer_key, digest_key):
    params = {
        'oauth_consumer_key' : consumer_key, 
        'oauth_token' : oauth_token, 
        'oauth_signature_method' : 'HMAC-SHA1', 
        'oauth_timestamp' : str(int(time())), 
        'oauth_nonce' : str(getrandbits(64)),
        'oauth_version' : '1.0'}

    params['oauth_signature'] = get_sign('POST', 
                                         url,
                                         params,
                                         digest_key )
    print 'HOGE'
    uri = url
    print uri

    try:
        ret = urlopen(uri, urlencode(params))
        res = parse_qs(ret.read())
        print res
        if not res.has_key('oauth_token'):
            # TODO logging
            print 'a'
            return None
        if not res.has_key('oauth_token_secret'):
            # TODO logging
            print 'b'
            return None
        if not res.has_key('screen_name'):
            # TODO logging
            print 'c'
            return None
        if not res.has_key('user_id'):
            # TODO logging
            print 'd'
            return None

        return AccessToken(sid = sid, 
                           oauth_token = res['oauth_token'][0],
                           oauth_token_secret = res['oauth_token_secret'][0], 
                           time_created = datetime.now(), 
                           user_id = res['user_id'][0], 
                           screen_name = res['screen_name'][0])
    except IOError, e:
        # TODO logging
        print 'e'
        print e.args
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

