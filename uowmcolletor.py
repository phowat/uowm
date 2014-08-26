#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import walk
import pprint

def list_files(basedir):
    paths = []
    for dirpath,dirname,filenames in walk(basedir):
        paths += map(lambda x: (dirpath+"/"+x).replace(basedir,''), filenames)
    return paths

if __name__ == '__main__':
    paths = list_files("/home/pedro/wallpapers")
    pprint.pprint(paths)
