#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Unnecessarily Overengineered Wallpaper Manager

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
        from uowmconsole import WPConsole
        prev_cmd = ""
        console = WPConsole(dirs=options.directories)
        console.cmdloop()
        """
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
        """
    else:
        change_wallpaper(options.directories)
