#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Unnecessarily Overengineered Wallpaper Manager

import sys
from uowmlib import change_wallpaper
import argparse
from multiprocessing import Process, Value
from time import sleep, time

options = {}

""" --- TODO --- 
* Tornado server
* get one from same  "set"( dir for now) 
* web interface, show wallpapers, let user click to set
* tag wallpapers
* grade wallpapers
"""

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

    def change(self, split_args):
        dirs = split_args[1:] if len(split_args) > 1 else self.directories
        winner = change_wallpaper(dirs)
        self.last_change_ts.value = int(time()) 
        print winner
    
    def startloop(self, split_args):
        if len(split_args) > 1:
            sleep_secs = split_args[1]
        else:
            sleep_secs = 30
        print "Changing wallpaper every "+str(sleep_secs)+" seconds."
        self.loop_proc = Process(target=WPCmd.change_wallpaper_loop, 
                                 args=(sleep_secs, self.directories,
                                       self.last_change_ts))
        self.loop_proc.start()

    def endloop(self, split_args):
        print "Stopped automatic wallpaper change."
        self.__terminate_wallpaper_loop()

    def exit(self, split_args):
        print "So long and thanks for all the fish."
        self.__terminate_wallpaper_loop()
        sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server",
        action="store_true", dest="server", default=False,
        help="Starts uowm as a web server.")
    parser.add_argument("-c", "--cli",
        action="store_true", dest="cli", default=False,
        help="Starts as a cli.")
    parser.add_argument("directories",  nargs=argparse.REMAINDER, default=[])
    options = parser.parse_args()

    if options.server is True:
        from uowms import main
        main()
    elif options.cli is True:
        prev_cmd = ""
        cmd = WPCmd(options.directories)
        while 1:
            cur_cmd = raw_input("> ")
            if cur_cmd.strip() == "":
                cur_cmd = prev_cmd
            split_args = cur_cmd.split(' ')

            try:
                cmd_func = getattr(cmd, split_args[0])
            except AttributeError:
                print "Don't know how to do ["+str(cur_cmd)+"]."
            else:
                prev_cmd = cur_cmd
                cmd_func(split_args)
    else:
        change_wallpaper(options.directories)
