from google.appengine.ext import db

class User(db.Model):
    uid = db.IntegerProperty()
    name = db.StringProperty()
    screen_name = db.StringProperty()
