import os
import sys
sys.path.append(os.path.dirname( os.path.realpath( __file__ )) + '/lib')

from google.appengine.ext.webapp.util import run_wsgi_app
import cgi
import pprint
from google.appengine.ext import db
from gelodata.tweet import Tweet

def application ( environ, start_response ):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    form = cgi.FieldStorage(fp=environ['wsgi.input'], 
                            environ=environ)

    tweets = Tweet.all()
    for i in tweets:
        i.delete()
        
    return "OK"

def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
