#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from uowmlib import WPConfiguration, change_wallpaper
from multiprocessing import Process, Value, Array
from time import sleep, time

class WPCmd(object):

    def __init__(self, directories, collection):
        self.directories = directories
        self.loop_proc = None
        self.last_change_ts = Value('i', 0)
        self.collection = Array('c', 64)
        self.collection.value = collection

    @staticmethod
    def change_wallpaper_loop(sleep_secs, wp_dirs, last_change_ts, collection):

        sleep_secs = int(sleep_secs)
        while 1:
            now = int(time())
            if now - last_change_ts.value >= sleep_secs:
                change_wallpaper(wp_dirs, collection.value)
                last_change_ts.value = now
            sleep(sleep_secs)
            
    def __terminate_wallpaper_loop(self):
        if self.loop_proc is not None:
            self.loop_proc.terminate()
            self.loop_proc = None

    def change(self, split_args):
        dirs = split_args if len(split_args) > 0 else self.directories
        winner = change_wallpaper(dirs, self.collection)
        self.last_change_ts.value = int(time()) 
        print winner
    
    def delay(self, seconds=30):
        self.last_change_ts.value = int(time())+int(seconds)

    def startloop(self, split_args):
        if self.loop_proc is None:
            if len(split_args) > 0:
                sleep_secs = split_args[0]
            else:
                sleep_secs = 30
            if len(split_args) > 1:
                self.collection.value = split_args[1]

            print "Changing wallpaper every {0} seconds from collection {1}.".\
                  format(str(sleep_secs), self.collection.value)
            self.loop_proc = Process(target=WPCmd.change_wallpaper_loop, 
                                     args=(sleep_secs, self.directories,
                                           self.last_change_ts,
                                           self.collection))
            self.loop_proc.start()

    def endloop(self, split_args=[]):
        print "Stopped automatic wallpaper change."
        self.__terminate_wallpaper_loop()

    def getconf(self, parameter):
        conf = WPConfiguration()
        if parameter == 'collection':
            return self.collection.value
        else: 
            try:
                return getattr(conf, parameter)
            except AttributeError:
                return "PARAMETER NOT FOUND"

    def setconf(self, parameter, value):
        conf = WPConfiguration()
        conf.set(parameter, value)

    def exit(self, split_args=[]):
        print "So long and thanks for all the fish."
        self.__terminate_wallpaper_loop()
        sys.exit()

