from google.appengine.ext import db

class User(db.Model):
    uid = db.IntegerProperty() # user id
    name = db.StringProperty() # display name
    screen_name = db.StringProperty() # account
    
    @classmethod
    def get_user(self, account):
        ret = None
        users = db.GqlQuery('SELECT * FROM User WHERE screen_name = \'' + account + '\'')
        if users.count() > 0:
            ret = users[0]
            return ret

    @classmethod
    def isStored(self, uid):
        ret = False
        users = db.GqlQuery('SELECT * FROM User WHERE uid = ' + str(uid)) 
        if users.count() > 0:
            ret = True
        return ret
