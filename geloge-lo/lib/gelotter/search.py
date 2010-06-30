import gelotter.common
from django.utils import simplejson as json

api_host = 'search.twitter.com'

def search(query, 
           lang = None, 
           rpp = None, 
           page = None, 
           since_id = None, 
           geocode = None, 
           since = None, 
           max_id = None
           ):
    # TODO json to constant
    param = {'q' : query}

    if lang:
        param['lang'] = lang
    if rpp:
        param['rpp'] = rpp
    if page:
        param['page'] = page
    if since_id:
        param['since_id'] = since_id
    if geocode:
        param['geocode'] = geocode
    if since:
        param['since'] = since
    if max_id:
        param['max_id'] = max_id
    
    body = gelotter.common.apicall(api_host, '/search', 'json' , param)

    data = None
    if body:
        data = json.loads(body)
    return data
