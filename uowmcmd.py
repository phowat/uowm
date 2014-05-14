#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from uowmlib import change_wallpaper
from multiprocessing import Process, Value
from time import sleep, time

class WPCmd(object):

    def __init__(self, directories):
        self.directories = directories
        self.loop_proc = None
        self.last_change_ts = Value('i', 0)

    @staticmethod
    def change_wallpaper_loop(sleep_secs, wp_dirs, last_change_ts):

        sleep_secs = int(sleep_secs)
        while 1:
            now = int(time())
            if now - last_change_ts.value >= sleep_secs:
                change_wallpaper(wp_dirs)
                last_change_ts.value = now
            sleep(sleep_secs)
            
    def __terminate_wallpaper_loop(self):
        if self.loop_proc is not None:
            self.loop_proc.terminate()
            self.loop_proc = None

    def change(self, split_args):
        dirs = split_args if len(split_args) > 0 else self.directories
        winner = change_wallpaper(dirs)
        self.last_change_ts.value = int(time()) 
        print winner
    
    def startloop(self, split_args):
        if self.loop_proc is None:
            if len(split_args) > 0:
                sleep_secs = split_args[0]
            else:
                sleep_secs = 30
            print "Changing wallpaper every "+str(sleep_secs)+" seconds."
            self.loop_proc = Process(target=WPCmd.change_wallpaper_loop, 
                                     args=(sleep_secs, self.directories,
                                           self.last_change_ts))
            self.loop_proc.start()

    def endloop(self, split_args=[]):
        print "Stopped automatic wallpaper change."
        self.__terminate_wallpaper_loop()

    def exit(self, split_args=[]):
        print "So long and thanks for all the fish."
        self.__terminate_wallpaper_loop()
        sys.exit()

