import os
import sys
sys.path.append(os.path.dirname( os.path.realpath( __file__ )) + '/lib')

from google.appengine.ext.webapp.util import run_wsgi_app
import cgi
from django.utils import simplejson as json
from gelodata.tweet import Tweet
from gelodata.user import User
from gelopics.thumbs import Thumbs

def application ( environ, start_response ):
    data = []
    num_limit = 10
    before_tid = None

    start_response('200 OK', [('Content-Type', 'text/plain')])
    form = cgi.FieldStorage(fp=environ['wsgi.input'], 
                            environ=environ)

    if not form.has_key('account'):
        return json.dumps(data)

    if form.has_key('limit'):
        try:
            num_limit = int(form['limit'].value)
        except:
            pass

    if form.has_key('before_tid'):
        try:
            before_tid = int(form['before_tid'].value)
        except:
            pass


    account = form['account'].value

    user = User.get_user(account)
    if not user:
        return json.dumps(data)

    tweets = Tweet.getTweetsByUser(user, num_limit, before_tid)
    for tw in tweets:
        tw_data = []
        tw_data.append(str(tw.time))
        tw_data.append(Thumbs.genThumbs(tw.text))
        if tw.lat and tw.lng:
            tw_data.append([tw.lng, tw.lat])
        else:
            tw_data.append(None)
        tw_data.append(tw.tid)
        data.append(tw_data)
        
    return json.dumps(data)
    
def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
