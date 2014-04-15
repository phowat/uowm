#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Unnecessarily Overengineered Wallpaper Manager

import sys
from uowmlib import change_wallpaper
import argparse

options = {}

""" --- TODO --- 
* Tornado server
* get one from same  "set"( dir for now) 
* web interface, show wallpapers, let user click to set
* tag wallpapers
* grade wallpapers
"""

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
                if len(split_args) > 2:
                    winner = change_wallpaper(split_args[1:])
                elif len(split_args) > 1:
                    winner = change_wallpaper(split_args[1:])
                else:
                    winner = change_wallpaper(options.directories)
                print winner
            elif split_args[0] == "exit":
                prev_cmd = cmd
                print "So long and thanks for all the fish."
                sys.exit()
            else:
                print "Don't know how to do ["+str(cmd)+"]."
    else:
        change_wallpaper(options.directories)
