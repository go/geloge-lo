import os
import sys
import pprint

sys.path.append(os.path.dirname( os.path.realpath( __file__ )) + '/../lib')

from google.appengine.ext.webapp.util import run_wsgi_app
from gelotter.account import rate_limit_status


def application ( environ, start_response ):
    start_response('200 OK', [('Content-Type', 'text/plain')])

    pprint.pprint(rate_limit_status())
    return

def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
