import os
import sys
sys.path.append(os.path.dirname( os.path.realpath( __file__ )) + '/../lib')
from google.appengine.ext.webapp.util import run_wsgi_app

import cgi
import Cookie
from urllib import quote
from datetime import datetime
from gelosession import GeloSession, getGeloSession
from gelotter.search import search
from gelotter.oauth import Token
from django.utils import simplejson as json

def application ( environ, start_response ):
    session = None
    
    form = cgi.FieldStorage(fp=environ['wsgi.input'], 
                            environ=environ)

    cookie = Cookie.SimpleCookie()

    if environ.has_key('HTTP_COOKIE'):
        cookie.load(environ["HTTP_COOKIE"])

    if form.has_key('hashname'):
        hashname = quote(form['hashname'].value)
    
    start_response('200 OK', [('Content-Type', 'text/plain')])
    ret = []
    for page in range(1,16):
      tweets = search(hashname, rpp="100", page=str(page))['results']

      for t in tweets:
          lat = None
          lng = None
          if t['geo']:
              lat = float(t['geo']['coordinates'][0])
              lng = float(t['geo']['coordinates'][1])
          elem = []
          elem.append(str(datetime.strptime(t['created_at'], "%a, %d %b %Y %H:%M:%S +0000")))
          elem.append(t['text'])
          if lat and lng:
              elem.append([lat, lng])
          ret.append(elem)

    return json.dumps(ret)

def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
