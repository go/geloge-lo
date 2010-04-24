import gelotter.common
from django.utils import simplejson as json

api_host = 'twitter.com'

def show(account):
    data = None
    body = gelotter.common.apicall(api_host, '/users/show/' + account, 'json' , { })
    if body:
        data = json.loads(body)
    return data

