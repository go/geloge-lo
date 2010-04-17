from google.appengine.ext import db

class Tweet(db.Model):
    uid = db.IntegerProperty()
    tid = db.IntegerProperty()
    text = db.StringProperty()
    lat = db.FloatProperty()
    lng = db.FloatProperty()
    time = db.DateTimeProperty()
    
    @classmethod
    def getTweetsByUser(self, user):
        tweets = db.GqlQuery('SELECT * FROM Tweet WHERE uid = ' + str(user.uid) + ' ORDER BY tid DESC')
        return tweets
        
    
