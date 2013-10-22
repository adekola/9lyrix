__author__ = 'adekola'

from google.appengine.ext import ndb
from google.appengine.ext.ndb import Model



class Song(Model):
    title = ndb.StringProperty()
    lyrics = ndb.TextProperty()
    year = ndb.IntegerProperty()
    remix = ndb.BooleanProperty(default=False)
    artist = ndb.StringProperty()

