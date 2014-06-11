#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Unnecessarily Overengineered Wallpaper Manager

import argparse

options = {}

""" --- TODO --- 
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
    parser.add_argument("-C", "--collection",
        dest="collection", default="default", 
        help="Use other collecion instead of default one")
    parser.add_argument("directories",  nargs=argparse.REMAINDER, default=[])
    options = parser.parse_args()

    directories = map(lambda(x): x.decode('utf8') if isinstance(x, str) else x,
                      options.directories)

    if options.server is True:
        from uowms import main
        main()
    else:
        from uowmconsole import WPConsole
        console = WPConsole(dirs=directories,
                            collection=options.collection)
        if options.cli is True:
            console.cmdloop()
        else:
            console.do_change(" ".join(directories))
