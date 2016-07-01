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
import csv
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
        self.response.write("こんにちは\n")
        f = open('stations.tsv', 'r')
        reader = csv.reader(f, delimiter='\t')
        net = multi_dimension_dict(2)
        notvisit = {}
        distance = {}
        for line in reader:
            i = 1
            while i+1 < len(line):
                station1 = line[i] 
                station2 = line[i+1]
                net[station1][station2] = 1
                net[station2][station1] = 1
                if notvisit.has_key(station1) == False:
                    notvisit[station1] = True
                    distance[station1] = MAX_DISTANCE
                i = i + 1
            if notvisit.has_key(station2) == False:
                notvisit[station2] = True
                distance[station2] = MAX_DISTANCE

        #self.response.write(str(distance).decode("string-escape"))
        self.response.write(str(notvisit).decode("string-escape"))

        
        prev = {} #the node before
        start = self.request.get("station1")
        prev.update({start : start})
        self.response.write(str(prev).decode("unicode-escape"))
        distance[self.request.get("station1")] = 0
        u = self.request.get("station1")
        while True:
            flag = 0
            mini = MAX_DISTANCE
            for k in notvisit.keys():
                if notvisit[k] == True:
                    if distance[k] < mini:
                        mini = distance[k]
                        u = k
            notvisit[u] = False  #visit u (with minimum distance from start)
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
            if flag == 0: break  #if all nodes in notvisit == False, finish the loop

        self.response.write(self.request.get("station1"))       
        v = self.request.get("station2")

        
        while v != self.request.get("station1"):
            self.response.write(prev[v])
            v = prev[v]
        self.response.write('Distance : %d' % distance[self.request.get("station2")])

                    
        
            
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/result', Result),
], debug=True)
