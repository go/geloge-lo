import os
import sys
sys.path.append(os.path.dirname( os.path.realpath( __file__ )) + '/../lib')
from google.appengine.ext.webapp.util import run_wsgi_app

from gelodata.tweet import Tweet

from datetime import datetime
from django.utils import simplejson as json

class TweetAlreadyStoredException(Exception): pass
    
def add_tweet(tweet_info):
    if Tweet.isStored(tweet_info['id']):
        raise TweetAlreadyStoredException

    lat = None
    lng = None
    if tweet_info['coordinates']:
        lat = float(tweet_info['coordinates']['coordinates'][0])
        lng = float(tweet_info['coordinates']['coordinates'][1])
        
    new_tweet = Tweet()
    new_tweet.uid = tweet_info['user']['id']
    new_tweet.tid = tweet_info['id']
    new_tweet.text = tweet_info['text']
    if lat and lng:
        new_tweet.lat = lat
        new_tweet.lng = lng
    new_tweet.time = datetime.strptime(tweet_info['created_at'], "%a %b %d %H:%M:%S +0000 %Y")

    new_tweet.put()

def application ( environ, start_response ):
    session = None
    
    start_response('200 OK', [('Content-Type', 'text/plain')])
    ret = []

    try:
        t = json.load(environ['wsgi.input'])
        add_tweet(t)

    except "already stored":
        return 'NG'        
    except Exception, e:
        print e
        return 'NG'


    return 'OK'

def main ():
  run_wsgi_app(application)

if __name__ == '__main__':
  main()
