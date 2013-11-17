__author__ = 'adekola'

from google.appengine.ext import ndb
from google.appengine.ext.ndb import Model


class Song(ndb.Model):
    title = ndb.StringProperty()
    lyrics_brief = ndb.StringProperty()
    lyrics_details = ndb.TextProperty()
    year = ndb.IntegerProperty()
    is_remix = ndb.BooleanProperty(default=False)
    artist = ndb.StringProperty()
    date_added = ndb.DateProperty(auto_now_add=True)


class ArtistSuggestion(ndb.Model):
    artist_name = ndb.StringProperty()


class TitleSuggestion(ndb.Model):
    title = ndb.StringProperty()

