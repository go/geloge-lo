from google.appengine.ext import db
from datetime import datetime
import uuid

def getGeloSession(id = None):
    if id:
        query = GeloSession.gql("WHERE id = :sid ", sid=id)
        if query.count() > 0:
            query[0].put()
            return query[0]

            
    ret =  GeloSession(id = str(uuid.uuid4()), 
                       time_created = datetime.now(), 
                       time_updated = datetime.now()
                       )
    ret.put()
    return ret




class GeloSession(db.Model):
    id = db.StringProperty(required=True)
    time_created = db.DateTimeProperty()
    time_updated = db.DateTimeProperty()
    token_key = db.ReferenceProperty()
    return_to = db.StringProperty()
