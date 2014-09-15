#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rethinkdb as r
import random
from uowmlib import WPConfiguration, WPLog
import mimetypes


#TODO: 
# Multiple tags and 
# Multiple tags or
# Display new ones( without a last display timestamp) 

class WPDBColletion(object):

    def __init__(self, tags, wpconf):
        #TODO: Reimplement cycle_dirs option as cycle_tags
        self.log = WPLog(wpconf)
        self.conf = wpconf
        self.file_list = []

        _conn = r.connect(db='uowm')
        cur = r.table('wallpapers').\
              filter(r.row['tags'].contains(tags[0])).run(_conn)
        for wallpaper in cur:
            fullpath = wallpaper['fullpath']
            (mime, enc) = mimetypes.guess_type(fullpath)
            if mime is None:
                try:
                    mime = magic.from_file(fullpath, mime=True).split("/")[0]
                except UnicodeDecodeError:
                    print "Unable to determine mime type for"+fullpath
                    continue

            filetype = mime.split("/")[0]
            if filetype == 'image':
                self.file_list.append(fullpath)

    def draw(self):
        chosen = None
        while chosen is None:
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

def simple_drwa():
    _conn = r.connect(db='uowm')
    cur = r.table('wallpapers').\
          filter(r.row['tags'].contains("earthporn")).run(_conn)
    collection = []
    for cu in cur:
        collection.append(cu)
    print random.choice(collection)
if __name__ == '__main__':
    conf = WPConfiguration()
    a = WPDBColletion(['earthporn'], conf)
    print a.draw()
