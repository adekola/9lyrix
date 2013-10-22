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

import webapp2
import json
import crud
import os
import webapp2
import cgi
from google.appengine.api import users
from google.appengine.ext.webapp import template
from util.sessions import Session
import crud

session = Session()


class MainHandler(webapp2.RequestHandler):
    def get(self):
        """


        """
        self.response.write('Hello world!')


class IndexHandler(webapp2.RequestHandler):
    def get(self):
        #return the web page for landing page
        render(self, "index.html")


class addLyrics(webapp2.RequestHandler):
    def post(self):
        year = int(self.request.get("year"))
        artist = self.request.get("artist")
        remix = self.request.get("remix")
        if remix == "Yes":
            is_remix = True
        else:
            is_remix = False
        title = self.request.get("title")
        lyrics = self.request.get("lyrics")
        result = crud.add_lyrics(_artist=artist, _year=year, _remix=is_remix, _title=title, _lyrics=lyrics)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(result))
        #shld yu really be returning this? well, lets see how we can manipulate it on the client

    def get(self):
        """


        """
        pass


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
        """


        """
        pass


class getLyricsByArtist(webapp2.RequestHandler):
    def get(self):
        """


        """
        request = self.request.body()
        data = json.loads(request)
        artist = data["artist"]
        songs_result = crud.get_lyrics_by_artist(artist)
        self.response.write(json.dumps(songs_result))

    def post(self):
        """


        """
        pass


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


app = webapp2.WSGIApplication([
    ('/', IndexHandler), ('/addLyrics', addLyrics), ('/getLyricsByTitle', getLyricsByTitle), ('/getLyricsByArtist', getLyricsByArtist)
], debug=True)
