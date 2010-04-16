from google.appengine.ext.webapp.util import run_wsgi_app
import cgi
from gelotter.users import show
from gelodata.user import User

def application ( environ, start_response ):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    form = cgi.FieldStorage(fp=environ['wsgi.input'], 
                            environ=environ)

    if not form.has_key('account'):
        return "please input account"
    
    account = form['account'].value

    user = User.get_user(account)
    if not user:
        user = User()

    user_info = show(account)


    user.uid = user_info['id']
    user.name = user_info['name']
    user.screen_name = user_info['screen_name']

    user.put()
    
    return "OK"


def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
