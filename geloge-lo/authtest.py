import os
import sys
sys.path.append(os.path.dirname( os.path.realpath( __file__ )) + '/lib')
from google.appengine.ext.webapp.util import run_wsgi_app

import geloauth.request_token
from geloauth.session import getGeloSession
from geloauth.access_token import AccessToken

import Cookie
from datetime import datetime
import gelotter.account
def application ( environ, start_response ):
    temp_cred_req_uri = 'http://twitter.com/oauth/request_token'
    authz_uri = 'http://twitter.com/oauth/authorize'
    consumer_key = 'NB8p5RcwbfxqoroV22aNKg'
    consumer_secret = 'b9MgdPxkS4lbbNzyrOTId3P36UTwnwed7KXNiI0E0I'
    
    #form = cgi.FieldStorage(fp=environ['wsgi.input'], 
    #environ=environ)
    session = None

    cookie = Cookie.SimpleCookie()
    if environ.has_key('HTTP_COOKIE'):
        cookie.load(environ["HTTP_COOKIE"])

    if cookie.has_key('sid'):
        session = getGeloSession(cookie['sid'].value)
    else:
        session = getGeloSession()
        req_token = geloauth.request_token.get_request_token(session.id, 
                                                                 temp_cred_req_uri, 
                                                                 consumer_key, 
                                                                 consumer_secret)
        if not req_token:
            start_response('503 Service Unavailable', 
                           [('Content-Type',  'text/plain')])
            return 'can\'t get request token'

            
        req_token.put()
        start_response('302 Found', 
                       [('Content-Type',  'text/plain'), 
                        ('Set-Cookie',  'sid=' + session.id), 
                        ('Location', authz_uri + 
                         '?oauth_token=' + 
                         req_token.oauth_token)])
        return 'please authorize me!'



    session.time_updated = datetime.now()
    session.put()

    start_response('200 OK', [
            ('Content-Type',  'text/plain'), 
            ('Set-Cookie',  'sid=' + session.id)
            ])
    contents = ['cookie is ',   session.id]

    acc_token = AccessToken.gql("WHERE sid = :sid", 
                                sid=session.id).get()
    print acc_token
    if acc_token:
        contents.append(acc_token.screen_name)
    contents.append(str(session.time_created))
    contents.append(str(session.time_updated))
    print gelotter.account.rate_limit_status()
    print gelotter.account.rate_limit_status2(consumer_key, 
                                              consumer_secret, 
                                              acc_token.oauth_token, 
                                              acc_token.oauth_token_secret)

    return "\n".join(contents)

def main ():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()

