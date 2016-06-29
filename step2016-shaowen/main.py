#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import os
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class BaseHandler(webapp2.RequestHandler):
    def render(self, html, values={}):
        template = JINJA_ENVIRONMENT.get_template(html)
        self.response.write(template.render(values))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        i = 0
        while i < min(len(self.request.get("word1")), len(self.request.get("word2"))):
            self.response.write(self.request.get("word1")[i])
            self.response.write(self.request.get("word2")[i])
            i = i+1
        if i < len(self.request.get("word1")):
            while i < len(self.request.get("word1")):
               self.response.write(self.request.get("word1")[i]) 
               i = i+1
        elif i < len(self.request.get("word2")):
            while i < len(self.request.get("word2")):
               self.response.write(self.request.get("word2")[i]) 
               i = i+1
        else:
            pass

class Test(BaseHandler):
    def get(self):
        self.render('main.html')
               
app = webapp2.WSGIApplication([
    ('/', Test),
    ('/result',MainHandler),
], debug=True)
