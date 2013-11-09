#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json
import os

import webapp2
from google.appengine.ext.webapp import template

from logic import crud
from util.sessions import Session
from google.appengine.api import users
from handlers import base_handler

# You should seriously find a means of Extracting a method to prepare the response to each request based on the
# peculiarities of that request..i.e. refactor the call to set_status(), getResponseMessage() and self.response.write()

session = Session()

class IndexHandler(base_handler.BaseHandler):
    def get(self):
        #return the web page for landing page
        render(self, "index.html")

class AdminHandler(base_handler.BaseHandler):
        def get(self):
            user = users.get_current_user()
            if users.is_current_user_admin():
                user_data = {"user_id": user.user_id(), "name": user.nickname(), "logout_url": users.create_logout_url('/')}
                render(self, "admin.html", user_data)
            else:
                login_url = users.create_login_url('/admin')
                data = {"login_url": login_url}
                render(self, "admin.html", data)

class addLyrics(base_handler.BaseHandler):
    def post(self):
        request = self.request.body
        data = json.loads(request)
        lyrics_text = data["lyrics"]
        song_id = data["song_id"]
        result = crud.add_lyrics(lyrics_text,song_id)
        self.render_response(result, 201)
        #shld yu really be returning this? well, lets see how we can manipulate it on the client

    def get(self):
        self.render_response({}, 405)

class getLyricsByTitle(base_handler.BaseHandler):
    def get(self):
        """


        """
        title = self.request.get('title')
        song_details = crud.get_lyrics_with_title(title.lower())
        self.render_response(song_details, 200)

    def post(self):
        self.render_response({}, 405)

class addSong(base_handler.BaseHandler):
    def post(self):
        request = self.request.body
        data = json.loads(request)
        lyrics_text = data["lyrics"]
        year = int(data["year"])
        artist = data["artist"]
        remix = bool(data["remix"])
        title = data["title"]
        if data.keys().__contains__('lyrics'):
            result = crud.add_song(_year=year, _artist=artist, _title=title, _is_remix=remix, lyrics=lyrics_text)
        else:
            result = crud.add_song(_artist=artist, _year=year, _is_remix=remix, _title=title)

        self.render_response(result, 201)

class getSongsByGenre(base_handler.BaseHandler):
    def post(self):
        self.render_response({}, 405)

    def get(self):
        pass

class getLyricsByArtist(base_handler.BaseHandler):
    def get(self):
        """


        """
        artist = self.request.get('artist')
        lyrics_result = crud.get_lyrics_by_artist(artist.lower())
        self.render_response(lyrics_result, 200)

    def post(self):
        """


        """
        self.render_response({}, 405)

class getSongsByTitle(base_handler.BaseHandler):
    def post(self):
        """The POST method is not allowed on this URL"""
        self.render_response({}, 405)

    def get(self):
        """Yes, this URL accepts a GET method and returns a response as appropriate"""
        request = self.request.body
        data = json.loads(request)
        title = data["title"]
        songs_result = crud.get_songs_with_title(title)
        response = {"response": songs_result}
        self.render_response(response,200)

class getSongsByArtist(base_handler.BaseHandler):
    def get(self):
        request = self.request.body()
        data = json.loads(request)
        artist = data["artist"]

    def post(self):
        self.render_response({},405)

class getAllSongs(base_handler.BaseHandler):
    def get(self):
        songs_result = crud.get_all_songs()
        response = {"response": songs_result}
        self.render_response(response, 200)

def render(handler, template_file="index.html", data={}):
    """

    :param handler:
    :param template_file:
    :param data:
    :return:
    """
    temp = os.path.join(
        os.path.dirname(__file__),
        'templates/' + template_file)
    if not os.path.isfile(temp):
        return False

    # Make a copy of the dictionary and add the path and session
    newval = dict(data)
    newval['path'] = handler.request.path
    handler.session = session

    #love this part
    outStr = template.render(temp, data)
    handler.response.out.write(unicode(outStr))
    return True


#how do you authorize the apps that will be calling yur API
app = webapp2.WSGIApplication([
                                  ('/', IndexHandler),
                                  ('/admin/', AdminHandler),
                                  ('/v1/song/', addSong),
                                  ('/v1/songs/', getAllSongs),
                                  ('/v1/songs/', getSongsByGenre),
                                  ('/v1/lyrics/', addLyrics),
                                  ('/v1/lyrics/byArtist', getLyricsByArtist), #mobile client
                                  ('/v1/lyrics/byTitle', getLyricsByTitle), #mobile client
                                  ('/v1/songs/title', getSongsByTitle),
                                  ('/v1/songs/artist', getSongsByArtist)
                              ], debug=True)
