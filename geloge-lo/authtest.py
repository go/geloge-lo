import os
import sys
sys.path.append(os.path.dirname( os.path.realpath( __file__ )) + '/lib')
from google.appengine.ext.webapp.util import run_wsgi_app

from geloauth.session import getGeloSession
import Cookie
from datetime import datetime
def application ( environ, start_response ):
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

    session.time_updated = datetime.now()
    session.put()
    start_response('200 OK', [
            ('Content-Type',  'text/plain'), 
            ('Set-Cookie',  'sid=' + session.id)
            ])
    contents = ['cookie is ',   session.id]
    if session.username:
        contents = contents + session.username
    contents.append(str(session.time_created))
    contents.append(str(session.time_updated))
    return contents

def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()


