#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import walk
import pprint
import time

def list_files(basedir):
    paths = []
    for dirpath,dirname,filenames in walk(basedir):
        paths += map(lambda x: [dirpath, x], filenames)
    return paths

def extract_tags(basedir, path):
    return filter(lambda x: len(x) > 0, path.replace(basedir,'').split("/"))

def create_structure(basedir, path):
    return {
        'fullpath': path[0]+'/'+path[1],
        'name': path[1],
        'tags': extract_tags(basedir, path[0]),
        'added': int(time.time()),
        'last_display': 0,
    }

def create_structures(basedir, paths):
    return map(lambda x: create_structure(basedir, x), paths)

if __name__ == '__main__':
    basedir = "/home/pedro/wallpapers";
    paths = list_files(basedir)
    db_struct = create_structures(basedir, paths)
    pprint.pprint(db_struct)
