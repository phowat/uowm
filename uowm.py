#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Unnecessarily Overengineered Wallpaper Manager

import sys
from uowmlib import change_wallpaper
import argparse
from multiprocessing import Process, Value
from time import sleep, time

options = {}
loop_proc = None
last_change_ts = Value('i', 0)

""" --- TODO --- 
* Tornado server
* get one from same  "set"( dir for now) 
* web interface, show wallpapers, let user click to set
* tag wallpapers
* grade wallpapers
"""

def change_wallpaper_loop(sleep_secs, wp_dirs, last_change_ts):
    sleep_secs = int(sleep_secs)
    while 1:
        now = int(time())
        if now - last_change_ts.value >= sleep_secs:
            change_wallpaper(wp_dirs)
            last_change_ts.value = now
        sleep(sleep_secs)
        
def terminate_wallpaper_loop():
    global loop_proc
    if loop_proc is not None:
        loop_proc.terminate()

def cmd_change(split_args, directories):
    global last_change_ts
    dirs = split_args[1:] if len(split_args) > 1 else directories
    winner = change_wallpaper(dirs)
    last_change_ts.value = int(time()) 
    print winner

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
        while 1:
            cmd = raw_input("> ")
            if cmd.strip() == "":
                cmd = prev_cmd

            split_args = cmd.split(' ')
            if split_args[0] == "change":
                prev_cmd = cmd
                cmd_change(split_args, options.directories)

            elif split_args[0] == "startloop":
                prev_cmd = cmd
                if len(split_args) > 1:
                    sleep_secs = split_args[1]
                else:
                    sleep_secs = 30
                print "Changing wallpaper every "+str(sleep_secs)+" seconds."
                loop_proc = Process(target=change_wallpaper_loop, 
                                    args=(sleep_secs, options.directories,
                                        last_change_ts))
                loop_proc.start()
            elif split_args[0] == "endloop":
                prev_cmd = cmd
                print "Stopped automatic wallpaper change."
                terminate_wallpaper_loop()
            elif split_args[0] == "exit":
                print "So long and thanks for all the fish."
                terminate_wallpaper_loop()
                sys.exit()
            else:
                print "Don't know how to do ["+str(cmd)+"]."
    else:
        change_wallpaper(options.directories)
