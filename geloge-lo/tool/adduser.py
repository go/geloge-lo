from google.appengine.ext.webapp.util import run_wsgi_app
import cgi
import pprint
from gelodata.user import User

def application ( environ, start_response ):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    form = cgi.FieldStorage(fp=environ['wsgi.input'], 
                            environ=environ)

    if not form.has_key('name'):
        return "please input name"
        
    user = User()
    if form.has_key('uid'):
        user.uid = int(form['uid'].value)
    user.name = form['name'].value
    if form.has_key('screen_name'):
        user.screen_name = form['screen_name'].value
    user.put()
    
    return "OK"


def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
