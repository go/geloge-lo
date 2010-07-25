import os
import sys
sys.path.append(os.path.dirname( os.path.realpath( __file__ )) + '/../lib')

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api.labs.taskqueue import Task
import pprint
from google.appengine.ext import db
from gelodata.user import User
from django.utils import simplejson as json


def application ( environ, start_response ):
    start_response('200 OK', [('Content-Type', 'text/plain')])

    users = db.GqlQuery('SELECT * FROM User')
    for user in users:
        ret.append(user.uid)
    return json.dumps(ret)

def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
