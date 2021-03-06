#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rethinkdb as r
import random
from uowmlib import WPConfiguration, WPLog, is_image
import mimetypes
import json


#TODO: 
# Multiple tags and 
# Multiple tags or
# Display new ones( without a last display timestamp) 

class WPDBColletion(object):

    def __init__(self, tags, wpconf, tag_match="AND"):
        def match_or(wp):
            for tag in wp['tags']:
                if r.expr(tags).contains(tag):
                    return True
            return False

        #TODO: Reimplement cycle_dirs option as cycle_tags
        self.log = WPLog(wpconf)
        self.conf = wpconf
        self.file_list = []

        _conn = r.connect(db='uowm')
        t = r.table('wallpapers')
        f = r.row['tags']
        if tag_match == 'OR':
            cur = []
            for tag in tags:
                cur += [x for x in t.filter(f.contains(tag)).run(_conn)]
        else: #AND
            cur = t.filter(f.contains(*tags)).run(_conn)

        for wallpaper in cur:
            fullpath = wallpaper['fullpath']
            if is_image(fullpath):
                self.file_list.append(fullpath)

    def draw(self):
        chosen = None
        while chosen is None:
            print len(self.file_list)
            candidate = random.choice(self.file_list)
            if len(self.file_list) > self.conf.no_repeat:
                if not self.log.in_last(self.conf.no_repeat, candidate):
                    chosen = candidate
            else:
                print "This collection has less items than the no_repeat \
parameter. We cannot guarantee this."
                chosen = candidate
        self.log.add(chosen)
        return chosen

def simple_draw():
    _conn = r.connect(db='uowm')
    cur = r.table('wallpapers').\
          filter(r.row['tags'].contains("earthporn")).run(_conn)
    collection = []
    for cu in cur:
        collection.append(cu)
    print random.choice(collection)
if __name__ == '__main__':
    conf = WPConfiguration()
    a = WPDBColletion(['earthporn', 'comics'], conf, tag_match="OR")
    b = WPDBColletion(['earthporn'], conf, tag_match="AND")
    print a.draw()
    print b.draw()
