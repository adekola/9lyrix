__author__ = 'adekola'
"""
This module does the db access functions for the 9lyrix platform...here are a bunch of functions for various db access tasks
"""

from models.models import Song
from google.appengine.api import users


# def add_lyrics(lyrics_text, song_id):
#     """
#     method to add a new song with its details to the data store
#
#     :param _artist: The name of the artiste who recorded the song (Indicate a collaboration by entering ABC ft. XYZ and MNO)
#     :param _year: The year the song was released (e.g. 2013)
#     :param _title: The title of the song
#     :param _remix: An indication of whether the song is a remix or not - True if it is a remix and False if not
#     :param _lyrics: The lyrics of the song -  a Text property so it can accommodate lengthy lyrics
#     :return: a Song object i.e. the newly created song
#     """
#     lyric = Lyrics()
#     lyric.added_by = users.get_current_user()
#     lyric.lyrics_text = lyrics_text
#     lyric.is_approved = users.is_current_user_admin() #aproved if the user is admin, else not
#     key = lyric.put()
#     lyric_id = str(key.id())
#     song = Song.get_by_id(song_id)
#     song.lyric_id = lyric_id
#     song.put()
#     result = \
#         {
#             "lyrics_text": lyrics_text,
#             "song_id": song_id,
#             "lyric_id": lyric_id,
#         }
#     return result
#

def add_song(_year, _artist, _title, _is_remix, lyrics):
    song = Song()
    song.artist = _artist
    song.year = _year
    song.is_remix = _is_remix
    song.title = _title
    song.lyrics = lyrics
    key = song.put()
    song_id = key.id()
    result = \
        {
            "title": _title,
            "song_id": song_id,
            "year": _year,
            "is_remix": _is_remix,
            "artist": _artist,
            "lyrics": lyrics
        }

    return result


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


def get_songs_with_title(_title):
    query = Song.query(Song.title == _title).get()
    songs_list = list()
    if len(query) > 0:
        for song in query:
            #add a dictionary representation of the song to list
            songs_list.append(song.to_dict)
        #empty if not populated by the
    return songs_list


def get_songs_by_artist(_artist):
    query = Song.query(Song.artist == _artist).get()
    songs_list = list()
    if len(query) > 0:
        for song in query:
            #add a dictionary representation of the song to list
            songs_list.append(song.to_dict)
        #empty if not populated by the
    return songs_list


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


def get_lyrics_by_artist(_artist):
    songs_query = Song.query(Song.artist == _artist).fetch()
    songs_result = list()
    if len(songs_query) > 0:
        for s in songs_query:
            song = {"artist": s.artist, "title": s.title, "year": s.year, "remix": s.is_remix, "lyrics": s.lyrics}
            songs_result.append(song)
            return songs_result

    else:
        return {}

#review this to allow for multiple matches
def get_lyrics_with_title(_title):
    songs = Song.query(Song.title == _title).fetch()
    if len(songs) > 0 :
        song_match = songs[0]
        song_details = {"title": song_match.title,
                        "remix": song_match.is_remix,
                        "artist": song_match.artist,
                        "year": song_match.year,
                        "lyrics": song_match.lyrics
        }

        return song_details
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

