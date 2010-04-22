import os
import sys
sys.path.append(os.path.dirname( os.path.realpath( __file__ )) + '/lib')

from google.appengine.ext.webapp.util import run_wsgi_app
import cgi
import pprint
from gelodata.tweet import Tweet

def application ( environ, start_response ):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    form = cgi.FieldStorage(fp=environ['wsgi.input'], 
                            environ=environ)
    if not form.has_key('uid'):
        return "please input uid"
    if not form.has_key('tid'):
        return "please input tid"
    if not form.has_key('text'):
        return "please input text"
    if not form.has_key('lat'):
        return "please input lat"
    if not form.has_key('lng'):
        return "please input lng"

    tweet = Tweet()
    tweet.uid = int(form['uid'].value)
    tweet.tid = int(form['tid'].value)
    tweet.text = form['text'].value
    tweet.lat = float(form['lat'].value)
    tweet.lng = float(form['lng'].value)

    tweet.put()
    
    return "OK"


def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
