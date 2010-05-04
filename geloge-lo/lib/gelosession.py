from google.appengine.ext import db
from datetime import datetime
import uuid
import Cookie

class GeloSession(db.Model):
    id = db.StringProperty(required=True)
    time_created = db.DateTimeProperty()
    time_updated = db.DateTimeProperty()
    token_key = db.ReferenceProperty()
    return_to = db.StringProperty()

def getGeloSession(id):
    query = GeloSession.gql("WHERE id = :sid ", sid=id)
    if query.count() == 0:
        return None
    return query[0]

def getAuthorizedGeloSession(id):
    session = getGeloSession(id)
    if not session:
        return None
    if not session.token_key:
        return None
    if not session.token_key.screen_name:
        return None

    return session

def createGeloSession():
    ret =  GeloSession(id = str(uuid.uuid4()), 
                       time_created = datetime.now(), 
                       time_updated = datetime.now()
                       )
    ret.put()
    return ret

def loadCookie(cookie_str):
    cookie = Cookie.SimpleCookie()
    if cookie_str:
        cookie.load(cookie_str)
    return cookie

def getSessionId(cookie):
    if cookie.has_key('sid'):
        return cookie['sid'].value
    else:
        return None

def getGeloSessionByEnviron(environ):
    return __getGeloSessionByEnviron(environ, getGeloSession)

def getAuthorizedGeloSessionByEnviron(environ):
    return __getGeloSessionByEnviron(environ, getAuthorizedGeloSession)

def __getGeloSessionByEnviron(environ, getSessionMethod):
    session = None
    if not environ.has_key('HTTP_COOKIE'):
        return None
    
    cookie = loadCookie(environ['HTTP_COOKIE'])
    
    session = getSessionMethod(getSessionId(cookie))

    return session
