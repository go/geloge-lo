import os
import sys
sys.path.append(os.path.dirname( os.path.realpath( __file__ )) + '/../lib')

from google.appengine.ext.webapp.util import run_wsgi_app
import cgi
import pprint
from google.appengine.ext import db
from gelodata.user import User
import logging

def application ( environ, start_response ):
    logging.getLogger().setLevel(logging.INFO)

    start_response('200 OK', [('Content-Type', 'text/plain')])
    form = cgi.FieldStorage(fp=environ['wsgi.input'], 
                            environ=environ)
    if not form.has_key('account'):
        return "please input account"

    qs = 'SELECT * FROM User WHERE screen_name = \'' + form['account'].value + '\''
    logging.info(qs)
    user = db.GqlQuery(qs)[0]
    print user
    print user.uid
    print user.name
    print user.screen_name
    

    return "OK"


def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
