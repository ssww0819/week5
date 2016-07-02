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
import linecache

import json
from collections import defaultdict

MAX_DISTANCE = 100

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class BaseHandler(webapp2.RequestHandler):
    def render(self, html, values={}):
        template = JINJA_ENVIRONMENT.get_template(html)
        self.response.write(template.render(values))
        
class MainHandler(BaseHandler):
    def get(self):
        self.render('main.html')
        
def multi_dimension_dict(dimension):
    nodes = defaultdict(int)
    for i in range(dimension-1):
        lm = nodes.default_factory
        nodes = defaultdict(lambda : defaultdict(lm))
    return nodes
    
class Result(webapp2.RequestHandler):
    def get(self):
        self.response.write("route : \n")
        f1 = open('net.json', 'r')
        reader1 = json.load(f1)
        net = multi_dimension_dict(2)
        notvisit = {}
        distance = {}

        for j in range(0, len(reader1)):
            dict_line = reader1[j]
            if dict_line.has_key('Stations'):
                i = 0
                while i +1 < len(dict_line['Stations']):
                    station1 = dict_line['Stations'][i] 
                    station2 = dict_line['Stations'][i+1]
                    net[station1][station2] = 1
                    net[station2][station1] = 1
                    if notvisit.has_key(station1) == False:
                        notvisit[station1] = True
                        distance[station1] = MAX_DISTANCE
                    if notvisit.has_key(station2) == False:
                        notvisit[station2] = True
                        distance[station2] = MAX_DISTANCE
                    i += 1

        prev = {} #the node before
        start = self.request.get("station2")
        prev.update({start : start})
        distance[start] = 0
        u = []
        loop = 0
        while True:
            flag = 0
            mini = MAX_DISTANCE
            for k in notvisit.keys():
                if notvisit[k]== True:
                    if distance[k] < mini:
                        mini = distance[k]
                        u = k
            notvisit[u] = False  #visit u (with minimum distance from start)
            #self.response.write(u)
            for k in notvisit.keys():
                if notvisit[k] == True:
                    if net[u][k] == 1:
                        d_k = distance[u] + net[u][k]
                        if d_k < distance[k]:
                            distance[k] = d_k
                            prev.update({k : u})
                            #self.response.write(str(prev).decode("unicode-escape"))
            for k in notvisit.keys():
                if notvisit[k] == True:
                    flag = 1

            loop += 1
            if flag == 0: break  #if all nodes in notvisit == False, finish the loop
              
        v = self.request.get("station1")
        self.response.write(v)
        self.response.write('\n')
        while v != start:
            self.response.write(prev[v])
            self.response.write('\n')
            #print " <- %d" % prev[v]
            v = prev[v]
        
           
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/result', Result),
], debug=True)
