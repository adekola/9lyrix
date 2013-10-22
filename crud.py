__author__ = 'adekola'

from google.appengine.ext import ndb
from model import Song


def add_lyrics(_artist, _year, _title, _remix, _lyrics):
    """
    method to add a new song with its details to the data store

    :param _artist: The name of the artiste who recorded the song (Indicate a collaboration by entering ABC ft. XYZ and MNO)
    :param _year: The year the song was released (e.g. 2013)
    :param _title: The title of the song
    :param _remix: An indication of whether the song is a remix or not - True if it is a remix and False if not
    :param _lyrics: The lyrics of the song -  a Text property so it can accommodate lengthy lyrics
    :return: a Song object i.e. the newly created song
    """
    new_song = Song()
    new_song.artist = _artist
    new_song.lyrics = _lyrics
    new_song.year = _year
    new_song.title = _title
    new_song.remix = _remix
    id = new_song.put()
    song_result = {"artist": _artist, "year": _year, "lyrics": _lyrics, "remix": _remix, "title": _title, "id": id.id()}
    return song_result


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


def get_lyrics_by_artist(_artist):
    songs_query = Song.query(Song.artist == _artist)
    songs_result = list()
    if len(songs_query) > 0:
        for s in songs_query:
            song = {"artist": s.artist, "title": s.title, "year": s.year, "remix": s.remix, "lyrics": s.lyrics}
            songs_result.append(song)

    return songs_result


def get_song(_id):

    """
    get_song() method - to retrieve a song using its id

    :param _id:  the id of the song to get
    :return: the song that matches the supplied id OR None if no matching song was found
    """
    song = Song.get_by_id(_id)
    if song is not None:
        return song
    else:
        return None


def get_lyrics_with_title(_title):
    song = Song.query(Song.title == _title)
    if song is not None:
        song_details = {"title": song.title, "remix": song.remix, "artist": song.artist, "year": song.year, "lyrics": song.lyrics}
        return song_details
    else:
        return False
