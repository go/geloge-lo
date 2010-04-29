import os
import sys
import cgi
sys.path.append(os.path.dirname( os.path.realpath( __file__ )) + '/lib')
from google.appengine.ext.webapp.util import run_wsgi_app

from gelosession import getGeloSession

import Cookie
from datetime import datetime
import gelotter.account
import gelotter.oauth

def do_auth(return_to, start_response):
    session = getGeloSession()
    req_token = gelotter.oauth.request_token()
    if not req_token:
        start_response('503 Service Unavailable', 
                       [('Content-Type',  'text/plain')])
        return 'can\'t get request token'

            
    token_key = req_token.put()
    session.token_key = token_key
    session.return_to = return_to
    session.time_updated = datetime.now()
    session.put()
    start_response('302 Found', 
                   [('Content-Type',  'text/plain'), 
                    ('Set-Cookie',  'sid=' + session.id), 
                    ('Location', gelotter.oauth.authz_uri + 
                     '?oauth_token=' + 
                     req_token.oauth_token)])
    return 'please authorize me!'
    
def application ( environ, start_response ):
    session = None

    form = cgi.FieldStorage(fp=environ['wsgi.input'], 
                            environ=environ)

    return_to = ''
    if form.has_key('return_to'):
        return_to = form['return_to'].value

    cookie = Cookie.SimpleCookie()
    if environ.has_key('HTTP_COOKIE'):
        cookie.load(environ["HTTP_COOKIE"])

    if not cookie.has_key('sid'):
        return do_auth(return_to, start_response)

    session = getGeloSession(cookie['sid'].value)
    session.time_updated = datetime.now()
    session.put()

    if not session.token_key:
        return do_auth(return_to, start_response)

    if not session.token_key.screen_name:
        return do_auth(return_to, start_response)
    
    start_response('200 OK', [
            ('Content-Type',  'text/plain'), 
            ('Set-Cookie',  'sid=' + session.id)
            ])
    contents = ['cookie is ',   session.id]

    acc_token = session.token_key
    print acc_token
    if acc_token:
        if acc_token.screen_name:
            contents.append(acc_token.screen_name)

    contents.append(str(session.time_created))
    contents.append(str(session.time_updated))

    print gelotter.account.rate_limit_status()
    print gelotter.account.rate_limit_status2(acc_token.oauth_token, 
                                              acc_token.oauth_token_secret)
    
    return "\n".join(contents)

def main ():
  run_wsgi_app(application)


if __name__ == '__main__':
  main()

