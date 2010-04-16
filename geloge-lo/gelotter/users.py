import gelotter.common
from django.utils import simplejson as json

def show(account):
    body = gelotter.common.apicall('/users/show/' + account, 'json' , { })
    data = json.loads(body)
    return data

