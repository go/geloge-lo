from google.appengine.ext.webapp.util import run_wsgi_app
import cgi
import pprint
from google.appengine.ext import db
from gelodata.user import User

def application ( environ, start_response ):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    form = cgi.FieldStorage(fp=environ['wsgi.input'], 
                            environ=environ)
    if not form.has_key('name'):
        return "please input name"

    user = db.GqlQuery('SELECT * FROM User WHERE name = \'' + form['name'].value + '\'')[0]
    print user
    print user.uid
    print user.name
    print user.screen_name
    return "OK"


def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
