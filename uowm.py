#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Unnecessarily Overengineered Wallpaper Manager

import os
import sys
import random
from shell import shell
from time import time
from itertools import cycle
from ConfigParser import ConfigParser, NoOptionError


""" --- TODO --- 
* Tornado server
* Check if last change was less than a XXXX ago
* parameter for cronjob
* get one from same  "set"( dir for now) 
* web interface, show wallpapers, let user click to set
* tag wallpapers
* grade wallpapers
"""

class WPConfiguration(object):
    def __init__(self, confpath=None):
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

        self.append_default_dirs = self._bool_par('append_default_dirs', False)

        try:
            self.log_file = self._conf.get('general', 'log_file')
        except NoOptionError:
            self.log_file = homedir+"/.uowm/log"

        try:
            self.no_repeat = self._conf.get('general', 'no_repeat')
        except NoOptionError:
            self.no_repeat = 20 # Check previous 20 files for wallpaper repetition

        self.cycle_dirs = self._bool_par('cycle_dirs', False)

    def _bool_par(self, par_name, default_val=False):
        try:
            par_val = self._conf.get('general', par_name)
        except NoOptionError:
            par_val = default_val
        else:
            if par_val == 'YES':
                par_val = True
            elif par_val == 'NO':
                par_val = False
            else:
                print "[CONF] [WARNING] "+par_name+" should be YES|NO."
                par_val = False
        return par_val

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
        last_n = shell("tail -{0} {1}".format(str(n), self.conf.log_file))
        return last_n.output()
    def in_last(self, n, candidate):
        last_n = self.fetch_last(n)
        for line in last_n:
            filename = line.split(' ', 1)[1]
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
            for root, subFolders, files in os.walk(directory):
                for f in files:
                    self.file_list.append(os.path.join(root, f))

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


class WPBackendGsettings(object):
    def set_wallpaper(self, wpaper):
        # In case you don't have DBUS_SESSION_BUS_ADDRESS and/or
        # DISPLAY set. export it before running this script. 
        cmd = """\
/usr/bin/env gsettings set \
org.gnome.desktop.background picture-uri "file://{0}"\
        """.format(wpaper)
        os.system(cmd)
        

if __name__ == '__main__':
    conf = WPConfiguration()
    backend = WPBackendGsettings()
    collection = WPCollection(sys.argv[1:])
    winner = collection.draw()
    backend.set_wallpaper(winner)

