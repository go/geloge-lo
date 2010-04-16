from google.appengine.ext.webapp.util import run_wsgi_app
import cgi
import pprint
from google.appengine.ext import db
from gelodata.user import User

def application ( environ, start_response ):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    form = cgi.FieldStorage(fp=environ['wsgi.input'], 
                            environ=environ)
    if not form.has_key('uid'):
        return "please input uid"

    tweet = db.GqlQuery("SELECT * FROM Tweet WHERE uid = " + form['uid'].value)[0]
    print tweet
    print tweet.uid
    print tweet.tid
    print tweet.text
    print tweet.lat
    print tweet.lng

    return "OK"

def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
