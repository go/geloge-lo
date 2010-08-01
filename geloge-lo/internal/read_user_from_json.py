import os
import sys
sys.path.append(os.path.dirname( os.path.realpath( __file__ )) + '/../lib')
from google.appengine.ext.webapp.util import run_wsgi_app

from gelodata.user import User

from django.utils import simplejson as json

def add_user(user_info):
    new_user = User()
    new_user.uid = user_info['id']
    new_user.name = user_info['name']
    new_user.screen_name = user_info['screen_name']

    new_user.put()

def application ( environ, start_response ):
    session = None
    
    start_response('200 OK', [('Content-Type', 'text/plain')])
    ret = []

    try:
        t = json.load(environ['wsgi.input'])
        add_user(t)

    except Exception, e:
        print e
        return 'NG'


    return 'OK'

def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
