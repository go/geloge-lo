import os
import sys
sys.path.append(os.path.dirname( os.path.realpath( __file__ )) + '/lib')

import Cookie
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from gelosession import getGeloSession
import gelotter.oauth
def application ( environ, start_response ):
    session = None

    cookie = Cookie.SimpleCookie()

    if environ.has_key('HTTP_COOKIE'):
        cookie.load(environ["HTTP_COOKIE"])

    if cookie.has_key('sid'):
        session = getGeloSession(cookie['sid'].value)

    if not session:
        start_response('302 Found', [('Content-Type',  'text/plain'), 
                                     ('Location', 'http://geloge-lo.appspot.com/login?return_to=http://geloge-lo.appspot.com/incremental')])
        return 'need authenticate'

    if not session.token_key:
        start_response('302 Found', [('Content-Type',  'text/plain'), 
                                     ('Location', 'http://geloge-lo.appspot.com/login?return_to=http://geloge-lo.appspot.com/incremental')])
        return 'need authenticate'

    if not session.token_key.screen_name:
        start_response('302 Found', [('Content-Type',  'text/plain'), 
                                     ('Location', 'http://geloge-lo.appspot.com/login?return_to=http://geloge-lo.appspot.com/incremental')])
        return 'need authenticate'

    path = os.path.join(os.path.dirname(__file__), 'tmpl/incremental.tmpl')
    return template.render(path, {'screen_name': session.token_key.screen_name})


def main ():
    run_wsgi_app(application)
    

if __name__ == '__main__':
    main()
