import os
import sys
sys.path.append(os.path.dirname( os.path.realpath( __file__ )) + '/lib')

import Cookie
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from gelosession import getGeloSession, getAuthorizedGeloSessionByEnviron
from gelohttp import redirect_login_url

import gelotter.oauth
def application ( environ, start_response ):
    session = getAuthorizedGeloSessionByEnviron(environ)

    if not session:
        return redirect_login_url(start_response, environ)

    path = os.path.join(os.path.dirname(__file__), 'tmpl/incremental.tmpl')
    return template.render(path, {'screen_name': session.token_key.screen_name})


def main ():
    run_wsgi_app(application)
    

if __name__ == '__main__':
    main()
