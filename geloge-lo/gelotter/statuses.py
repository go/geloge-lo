import urllib2
import gelotter.common
import sys
from django.utils import simplejson as json

def user_timeline(uid):
    # TODO json to constant
    body = gelotter.common.apicall('/statuses/user_timeline', 'json' , uid)
    data = json.loads(body)
    return data
