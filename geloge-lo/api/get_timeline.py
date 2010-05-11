import os
import sys
sys.path.append(os.path.dirname( os.path.realpath( __file__ )) + '/../lib')
from google.appengine.ext.webapp.util import run_wsgi_app

import cgi
import Cookie
from datetime import datetime
from gelosession import GeloSession, getGeloSession
from gelotter.statuses import user_timeline2
from gelotter.oauth import Token
from django.utils import simplejson as json

def application ( environ, start_response ):
    session = None
    
    form = cgi.FieldStorage(fp=environ['wsgi.input'], 
                            environ=environ)

    cookie = Cookie.SimpleCookie()

    if environ.has_key('HTTP_COOKIE'):
        cookie.load(environ["HTTP_COOKIE"])

    if not cookie.has_key('sid'):
        return 'session not found'

    session = getGeloSession(cookie['sid'].value)
    session.time_updated = datetime.now()
    session.put()

    start_response('200 OK', [('Content-Type', 'text/plain')])
    tweets = user_timeline2(session.id, 
                            oauth_token = session.token_key.oauth_token, 
                            oauth_token_secret = session.token_key.oauth_token_secret)

    ret = []
    for t in tweets:
        lat = None
        lng = None
        if t['coordinates']:
            lat = float(t['coordinates']['coordinates'][0])
            lng = float(t['coordinates']['coordinates'][1])
        elem = []
        elem.append(str(datetime.strptime(t['created_at'], "%a %b %d %H:%M:%S +0000 %Y")))
        elem.append(t['text'])
        if lat and lng:
            elem.append([lat, lng])
        ret.append(elem)

    return json.dumps(ret)

def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
