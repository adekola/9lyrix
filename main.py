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

# You should seriously find a means of Extracting a method to prepare the response to each request based on the
# peculiarities of that request..i.e. refactor the call to set_status(), getResponseMessage() and self.response.write()

session = Session()

class IndexHandler(webapp2.RequestHandler):
    def get(self):
        #return the web page for landing page
        render(self, "index.html")

class addLyrics(webapp2.RequestHandler):
    def post(self):
        request = self.request.body()
        data = json.loads(request)
        lyrics_text = data["lyrics"]
        song_id = data["song_id"]
        result = crud.add_lyrics(lyrics_text,song_id)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.set_status(200)
        self.response.write(json.dumps(result))
        #shld yu really be returning this? well, lets see how we can manipulate it on the client


    def get(self):
        self.response.set_status(405, getResponseMessage('405'))

class getLyricsByTitle(webapp2.RequestHandler):
    def get(self):
        """


        """
        request = self.request.body()
        data = json.loads(request)
        title = data["title"]
        song_details = crud.get_lyrics_with_title(title)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(song_details))

    def post(self):
        self.response.set_status(405, getResponseMessage('405'))

class addSong(webapp2.RequestHandler):
    def post(self):
        request = self.request.body()
        data = json.loads(request)
        year = data["year"]
        artist = data["artist"]
        remix = data["remix"]
        title = data["title"]
        result = crud.add_lyrics(_artist=artist, _year=year, _remix=remix, _title=title)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.set_status(201, getResponseMessage('201'))
        self.response.write(json.dumps(result))

class getSongsByGenre(webapp2.RequestHandler):
    def post(self):
        self.response.set_status('405', getResponseMessage('405'))

    def get(self):
        pass

class getLyricsByArtist(webapp2.RequestHandler):
    def get(self):
        """


        """
        request = self.request.body()
        data = json.loads(request)
        artist = data["artist"]
        lyrics_result = crud.get_lyrics_by_artist(artist)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.set_status(200)
        self.response.write(json.dumps(lyrics_result))

    def post(self):
        """


        """
        self.response.set_status('405', getResponseMessage('405'))
        response = {"response": getResponseMessage(405)}
        self.response.write(json.dumps(response))

class getSongsByTitle(webapp2.RequestHandler):
    def post(self):
        """The POST method is not allowed on this URL"""
        self.response.set_status('405', getResponseMessage('405'))
        response = {"response": getResponseMessage(405)}
        self.response.write(json.dumps(response))

    def get(self):
        """Yes, this URL accepts a GET method and returns a response as appropriate"""
        request = self.request.body()
        data = json.loads(request)
        title = data["title"]
        songs_result = crud.get_songs_with_title(title)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.set_status(200)
        response = {"response": songs_result}
        self.response.write(response)

class getSongsByArtist(webapp2.RequestHandler):
    def get(self):
        request = self.request.body()
        data = json.loads(request)
        artist = data["artist"]

    def post(self):
        self.response.set_status('405', getResponseMessage('405'))
        response = {"response": getResponseMessage(405)}
        self.response.write(json.dumps(response))

def getResponseMessage(code):
    return {'201': 'Resource Successfully Created',
            '401': 'Unauthorized Request; Please make sure you are Authorized',
            '400': 'That was a bad request; Be sure to modify your request before retrying',
            '404': 'Resource was not found',
            '405': 'That method is not allowed on this resource. Please refer to the API documentation',
            '500': 'Internal Server Error; Please contact Admin if this persists',
            '204': 'No content to send'}[code]


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
                                  ('/v1/song', addSong),
                                  ('/v1/songs/genre/{genre}', getSongsByGenre),
                                  ('/v1/lyric', addLyrics),
                                  ('/v1/lyrics/artist/{artist}', getLyricsByArtist),
                                  ('/v1/lyrics/title/{title}', getLyricsByTitle),
                                  ('/v1/songs/title/{title}', getSongsByTitle),
                                  ('/v1/songs/artist/{artist}', getSongsByArtist)


                              ], debug=True)
