import os
import sys
sys.path.append(os.path.dirname( os.path.realpath( __file__ )) + '/lib')
from google.appengine.ext.webapp.util import run_wsgi_app

import Cookie
from cgi import parse_qs
from geloauth.session import getGeloSession
from geloauth.access_token import get_access_token

def application ( environ, start_response ):
    token_req_uri = 'http://twitter.com/oauth/access_token'
    consumer_key = 'NB8p5RcwbfxqoroV22aNKg'
    consumer_secret = 'b9MgdPxkS4lbbNzyrOTId3P36UTwnwed7KXNiI0E0I'

    session = None
    cookie = Cookie.SimpleCookie()
    if environ.has_key('HTTP_COOKIE'):
        cookie.load(environ["HTTP_COOKIE"])

    if cookie.has_key('sid'):
        session = getGeloSession(cookie['sid'].value)

    param = parse_qs(environ['QUERY_STRING'])

    if not param.has_key('oauth_token'):
        start_response('400 Bad Request', [('Content-Type',  'text/plain')])
        return 'oauth_token not found'

    
    # TODO remove req_tokennnr
    acc_token = get_access_token(session.id, 
                                 token_req_uri,
                                 param['oauth_token'][0], 
                                 consumer_key, 
                                 consumer_secret + '&')
    if(acc_token):
        acc_token.put()
    start_response('200 OK', [('Content-Type',  'text/plain')])
    print acc_token
    return "OK"

def main ():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()

