from google.appengine.ext import db

class Tweet(db.Model):
    uid = db.IntegerProperty()
    tid = db.IntegerProperty()
    text = db.StringProperty()
    lat = db.FloatProperty()
    lng = db.FloatProperty()
