__author__ = 'adekola'

from google.appengine.ext import ndb
from google.appengine.ext.ndb import Model


class Song(ndb.Model):
    title = ndb.StringProperty()
    lyric_id = ndb.IntegerProperty()
    year = ndb.IntegerProperty()
    is_remix = ndb.BooleanProperty(default=False)
    artist = ndb.StringProperty()
    date_added = ndb.DateProperty(auto_now_add=True)


class Lyrics(ndb.Model):
    lyrics_text = ndb.TextProperty()
    date_added = ndb.DateProperty(auto_now_add=True)
    #Whats the difference between auto_current_user_add and auto_current_user?
    added_by = ndb.UserProperty()
    is_approved = ndb.BooleanProperty(default=False)


class Lyrics_Note(ndb.Model):
    added_by = ndb.UserProperty()
    lyric_id = ndb.IntegerProperty()
    note_text = ndb.TextProperty()
    date_added = ndb.DateProperty(auto_now_add=True)
