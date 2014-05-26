#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from uowmlib import WPConfiguration, change_wallpaper, apply_wallpaper
from multiprocessing import Process, Value, Array
from time import sleep, time
import os

class WPCmd(object):

    def __init__(self, directories, collection):
        self.directories = directories
        self.loop_proc = None
        self.sleep_secs = 0
        self.last_change_ts = Value('i', 0)
        self.collection = Array('c', 64)
        self.collection.value = collection
        self._conf = WPConfiguration()

    @staticmethod
    def change_wallpaper_loop(sleep_secs, wp_dirs, last_change_ts, collection, 
                              wpconf):

        # right now, wpconf here is just a copy of the WPConfig object.
        # when I implement a reload method, this will need to change. TODO
        sleep_secs = int(sleep_secs)
        while 1:
            now = int(time())
            if now - last_change_ts.value >= sleep_secs:
                change_wallpaper(wp_dirs, collection.value, wpconf)
                last_change_ts.value = now
            sleep(1)
            
    def __terminate_wallpaper_loop(self):
        if self.loop_proc is not None:
            self.loop_proc.terminate()
            self.loop_proc = None
            self.sleep_secs = 0

    def change(self, split_args):
        dirs = map(
            lambda x: x if x[0] == '/' else self._conf.basedir+'/'+ x,
            split_args if len(split_args) > 0 else self.directories)
        if len(dirs) == 1 and os.path.isfile(dirs[0]):
            # Check if this is a file instead of collection
            apply_wallpaper(dirs[0], self._conf)
        else:
            winner = change_wallpaper(dirs, self.collection.value, self._conf)
            print winner
        
        self.last_change_ts.value = int(time()) 
    
    def delay(self, seconds=30):
        to_add = int(seconds) + \
                 (self.sleep_secs - (int(time()) - self.last_change_ts.value))
        self.last_change_ts.value = self.last_change_ts.value + to_add

    def startloop(self, split_args):
        if self.loop_proc is None:
            if len(split_args) > 0:
                self.sleep_secs = int(split_args[0])
            else:
                self.sleep_secs = 30
            if len(split_args) > 1:
                self.collection.value = split_args[1]

            print "Changing wallpaper every {0} seconds from collection {1}.".\
                  format(str(self.sleep_secs), self.collection.value)
            self.loop_proc = Process(target=WPCmd.change_wallpaper_loop, 
                                     args=(self.sleep_secs, self.directories,
                                           self.last_change_ts,
                                           self.collection, self._conf))
            self.loop_proc.start()

    def endloop(self, split_args=[]):
        print "Stopped automatic wallpaper change."
        self.__terminate_wallpaper_loop()

    def getconf(self, parameter):
        if parameter == 'collection':
            return self.collection.value
        else: 
            try:
                return getattr(self._conf, parameter)
            except AttributeError:
                return "PARAMETER NOT FOUND"

    def setconf(self, parameter, value):
        self._conf.set(parameter, value)

    def exit(self, split_args=[]):
        print "So long and thanks for all the fish."
        self.__terminate_wallpaper_loop()
        sys.exit()

