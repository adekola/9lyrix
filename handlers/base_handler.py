__author__ = 'adekola'


import json
import os

import webapp2
from google.appengine.ext.webapp import template

from logic import crud
from util.sessions import Session
from google.appengine.api import users

class BaseHandler(webapp2.RequestHandler):
    def render_response(self, result, response_code):
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers.add_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(result))
        self.response.set_status(response_code)


def getResponseMessage(code):
    return {'201': 'Resource Successfully Created',
            '401': 'Unauthorized Request; Please make sure you are Authorized',
            '400': 'That was a bad request; Be sure to modify your request before retrying',
            '404': 'Resource was not found',
            '405': 'That method is not allowed on this resource. Please refer to the API documentation',
            '500': 'Internal Server Error; Please contact Admin if this persists',
            '204': 'No content to send'}[code]
