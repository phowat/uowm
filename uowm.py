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
    parser.add_argument("directories",  nargs=argparse.REMAINDER, default=[])
    options = parser.parse_args()

    if options.server is True:
        from uowms import main
        main()
    else:
        change_wallpaper(options.directories)
