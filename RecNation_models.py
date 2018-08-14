from google.appengine.ext import ndb

class Event(ndb.Model):
    activity = ndb.StringProperty(required=True)
    location = ndb.StringProperty(required=True)
    
class User(ndb.Model):
    name = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    schedule = ndb.KeyProperty(Event, repeated=True)

class Post(ndb.Model):
    author = ndb.KeyProperty(User, required=True)
    content = ndb.StringProperty(required=True)
    time = ndb.DateTimeProperty(auto_now_add=True)
