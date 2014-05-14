#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import random
import subprocess
from time import time
from itertools import cycle
from ConfigParser import ConfigParser, NoOptionError
import magic
import rethinkdb as r
from socket import gethostname
import mimetypes
import uowmbackends 


class WPConfiguration(object):
    def __init__(self, confpath=None):
        _conn = r.connect(db='uowm')
        self._conf = ConfigParser()
        homedir = os.path.expanduser('~')
        if confpath is None:
            self._conf.read(homedir+'/.uowmrc')
        else:
            self._conf.read(confpath)
        try:
            default_dirs = self._conf.get('general', 'default_dirs')
        except NoOptionError:
            self.default_dirs = []
        else:
            self.default_dirs = filter(
                lambda x: len(x) > 0, default_dirs.split('\n'))

        confs = r.table('config').\
               filter(r.row['hostname'] == gethostname()).\
               limit(1).run(_conn)
        # TODO: There's gotta be a better way...
        conf = {}
        for c in confs:
            conf = c
            break
        self.append_default_dirs = conf.get('append_default_dirs', False)
        self.log_file = conf.get('log_file',homedir+"/.uowm/log")
        self.no_repeat = int(conf.get('no_repeat', 20))
        self.backend = conf.get('backend', 'Noop')
        self.cycle_dirs = conf.get('cycle_dirs', False)


class WPLog(object):

    def __init__(self):
        self.conf = WPConfiguration()
        # Make sure path exists
        logdir = self.conf.log_file[0:self.conf.log_file.rindex("/")]
        if not os.path.exists(logdir):
            try:
                os.makedirs(logdir)
            except OSError, (errno):
                if errno != errno.EEXIST:
                   raise 

    def add(self, filepath):
        timestamp = str(int(time()))
        line = "[{0}] {1}\n".format(timestamp, filepath)
        logfile = open(self.conf.log_file, 'a')
        logfile.write(line)
        logfile.close()

    def fetch_last(self, n):
        last_n = subprocess.Popen(
            ['tail', '-'+str(n), self.conf.log_file], 
            stdout=subprocess.PIPE).communicate()[0]
        last_n = filter(lambda x: len(x) > 0, last_n.split('\n'))
        return last_n

    def in_last(self, n, candidate):
        last_n = self.fetch_last(n)
        for line in last_n:
            try:
                filename = line.split(' ', 1)[1]
            except IndexError:
                #Corrupted log line. skip it.
                continue
            if candidate == filename:
                return True
        return False

class WPCollection(object):
    
    def __init__(self, directories):
        self.log = WPLog()
        self.conf = WPConfiguration()
        self.file_list = []
        if self.conf.append_default_dirs is True: 
            directories = directories + self.conf.default_dirs
        elif len(directories) < 1:
            if len(self.conf.default_dirs) < 1:
                raise RuntimeError("No wallpapers directories defined.")
            else:
                directories = self.conf.default_dirs

        if self.conf.cycle_dirs is True:
            directories = self._cycle_dirs(directories)

        for directory in directories:
            for root, subFolders, files in os.walk(directory, followlinks=True):
                for f in files:
                    fullpath = os.path.join(root, f)
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

        if len(self.file_list) < 1:
            raise RuntimeError("No wallpapers available in ."+str(directories))
            

    def _cycle_dirs(self, directories):
        retdir  = []
        last_file = self.log.fetch_last(1)
        if len(last_file) < 1:
            retdir.append(directories[0])
        else:
            prevfile = last_file[0].split(' ',1)[1]
            dircount = len(directories)
            dircycle = cycle(directories)
            for i in range(dircount):
                curdir = dircycle.next()
                if curdir == prevfile[:(len(curdir))]:
                    retdir.append(dircycle.next())
                    break
            if len(retdir) < 1:
                retdir.append(directories[0])

        return retdir

    def draw(self):
        chosen = None
        while chosen is None:
            candidate = random.choice(self.file_list)
            if not self.log.in_last(self.conf.no_repeat, candidate):
                chosen = candidate
        self.log.add(chosen)
        return chosen


def change_wallpaper(directories=[]):
    conf = WPConfiguration()
    try:
        backend = getattr(uowmbackends, 'WPBackend'+conf.backend)()
    except AttributeError:
        print "Backend "+conf.backend+" not found."
        sys.exit()
    collection = WPCollection(directories)
    winner = collection.draw()
    backend.set_wallpaper(winner)
    return winner
