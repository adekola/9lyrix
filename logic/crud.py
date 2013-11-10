__author__ = 'adekola'
"""
This module does the db access functions for the 9lyrix platform...here are a bunch of functions for various db access tasks
"""

from models.models import Song
from google.appengine.api import users

def getSongs(args):
    
    if 'title' in args.keys() or 'artist' in args.keys() and args["title"] != "" and args["artist"] != "":
        query= Song.query()
        if 'title' in args.keys():
            query = query.filter(Song.title == args['title'].lower())
        if 'artist' in args.keys():
            query = query.filter(Song.artist == args['artist'].lower())
    else:
        return []
    result = query.fetch(10)
    if result:
        if isinstance(result, Song):
            return result.to_dict(exclude=['date_added', ])
        else:            
            return [{'title': song.title, 'artist': song.artist, 'year': song.year, 'id': song.key.id(),
                           'remix': song.is_remix} for song in result]
    else:
        return []

def get_songs_with_title(_title):
    query = Song.query(Song.title == _title).fetch(10)
    if query:
        if isinstance(query, Song):
            return query.to_dict(exclude=['date_added', ])
        else:            
            return [{'title': song.title, 'artist': song.artist, 'year': song.year, 'id': song.key.id(),
                           'remix': song.is_remix} for song in query]
 
def get_songs_with_artist(_artist):
    query = Song.query(Song.artist == _artist).fetch(10)
    if query:
        if isinstance(query, Song):
            return query.to_dict(exclude=['date_added', ])
        else:            
            return [{'title': song.title, 'artist': song.artist, 'year': song.year, 'id': song.key.id(),
                           'remix': song.is_remix} for song in query]

def add_song(_year, _artist, _title, _is_remix, lyrics):
    song = Song()
    song.artist = _artist.lower()
    song.year = _year
    song.is_remix = _is_remix
    song.title = _title.lower()
    song.lyrics_details = lyrics
    song.lyrics_brief = lyrics[:50]  # First 50 characters
    key = song.put()
    song_id = key.id()
    result = \
        {
            "title": _title,
            "song_id": song_id,
            "year": _year,
            "is_remix": _is_remix,
            "artist": _artist,
            "lyrics_brief": lyrics[:20]
        }

    return result

def get_lyrics_details(song_id):
    song = Song.get_by_id(song_id)
    if song is not None:
        song_details = {"title": song.title, "remix": song.is_remix, "artist": song.artist, "year": song.year,
                       "lyrics_details": song.lyrics_details}
        return song_details

    else:
        return {}

def update_song(_id, _year, _artist, _lyrics):
    """
    update_song() method - to update the details of a song

    :param _id: the id of the song to be updated
    :param _year: the updated value of the year
    :param _artist: the updated value of the artist
    :param _lyrics: the updated value of the lyrics
    :return: The updated song as a Song object

    *Note* - The title of the song can't be changed...if you need to, delete the song and add it as a new entry
    """
    song = Song.get_by_id(_id)
    song.artist = _artist
    song.year = _year
    song.lyrics = _lyrics
    song.put()
    return song

def get_song(_id):
    """
    get_song() method - to retrieve a song using its id

    :param _id:  the id of the song to get
    :return: the song that matches the supplied id OR None if no matching song was found
    """
    song = Song.get_by_id(_id)
    if song is not None:
        return song.to_dict()
    else:
        return {}

def get_lyrics_for_song(_id):
    song = Song.get_by_id(_id)
    if song is not None:
        lyrics = get_lyrics_for_song(song.key.id())
        return lyrics.to_dict()
    else:
        return {}


def get_all_songs():
    songs = Song.query().fetch()
    songs_list = list()
    for song in songs:
        songs_list.append({'title': song.title, 'artist': song.artist, 'year': song.year, 'id': song.key.id(),
                           'remix': song.is_remix})

    return songs_list

