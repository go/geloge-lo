import gelotter.common
from django.utils import simplejson as json

api_host = 'twitter.com'

def show(account):
    body = gelotter.common.apicall(api_host, '/users/show/' + account, 'json' , { })
    data = json.loads(body)
    return data

