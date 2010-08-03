from google.appengine.ext import db

class Tweet(db.Model):
    uid = db.IntegerProperty()
    tid = db.IntegerProperty()
    text = db.StringProperty(multiline=True)
    lat = db.FloatProperty()
    lng = db.FloatProperty()
    time = db.DateTimeProperty()
    
    @classmethod
    def getTweetsByUser(self, user, limit = 1000, before_tid = None):
        query = 'SELECT * FROM Tweet WHERE uid = ' + str(user.uid)
        if before_tid:
            query += ' AND tid < ' + str(before_tid)

        query += ' ORDER BY tid DESC'
        query += ' LIMIT ' + str(limit)

        tweets = db.GqlQuery(query)
        return tweets
        
    @classmethod
    def isStored(self, tid):
        ret = False
        tweets = db.GqlQuery('SELECT * FROM Tweet WHERE tid = ' + str(tid) + ' ORDER BY tid DESC')
        if tweets.count() > 0:
            ret = True
        return ret
            
        
