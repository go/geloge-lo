from google.appengine.ext.webapp.util import run_wsgi_app
import cgi
from django.utils import simplejson as json
from gelodata.tweet import Tweet
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
        return "user not found"

    tweets = Tweet.getTweetsByUser(user)
    data = []
    for tw in tweets:
        tw_data = []
        tw_data.append('!title!')
        tw_data.append(tw.text)
        tw_data.append([tw.lat, tw.lng])
        data.append(tw_data)
    print json.dumps(data)

def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
