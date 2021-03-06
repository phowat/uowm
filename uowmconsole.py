#!/usr/bin/env python
# -*- coding: utf-8 -*-

import atexit
import os
import readline
import cmd
from uowmcmd import WPCmd
import sys

class WPConsole(cmd.Cmd):
    def __init__(self, dirs=[], collection=None,
                 histfile=os.path.expanduser("~/.uowm/history")):
        cmd.Cmd.__init__(self)
        self.prompt = ">> "
        self.intro = """
  888     888 .d88888b. 888       888888b     d888 
  888     888d88P" "Y88b888   o   8888888b   d8888 
  888     888888     888888  d8b  88888888b.d88888 
  888     888888     888888 d888b 888888Y88888P888 
  888     888888     888888d88888b888888 Y888P 888 
  888     888888     88888888P Y88888888  Y8P  888 
  Y88b. .d88PY88b. .d88P8888P   Y8888888   "   888 
   "Y88888P"  "Y88888P" 888P     Y888888       888 
   
    Unecessarily Overengineered Wallpaper Manager
        """
        self.histfile = histfile
        self.init_history()
        self.wpcmd = WPCmd(dirs, collection)


    def init_history(self):
        readline.parse_and_bind("tab: complete")
        if hasattr(readline, "read_history_file"):
            try:
                readline.read_history_file(self.histfile)
            except IOError:
                pass
            atexit.register(self.save_history)

    def save_history(self):
        readline.write_history_file(self.histfile)

    def postcmd(self, stop, line):
        self.save_history()

    def do_change(self, args):
        '[dir1 dir2 ...] - Changes current wallpaper once'
        if len(args):
            split_args = args.split(' ')
        else:
            split_args = []
        self.wpcmd.change(split_args)

    def do_startloop(self, args):
        '[interval collection] - Starts wallpaper change loop every N seconds'
        if len(args) > 0:
            split_args = args.split(' ')
        else:
            split_args = []
        self.wpcmd.startloop(split_args)

    def do_startloop_dirs(self, args):
        '[interval dir1 dir2 ...] - Starts wallpaper change loop every N seconds'
        if len(args) > 0:
            split_args = args.split(' ')
        else:
            split_args = []
        self.wpcmd.startloop(split_args, dirs=True)

    def do_delay(self, args):
        '[seconds] - Delays the execution of next change loop. Defaults to 30.'
        if len(args) > 0:
            delay = int(args)
        else:
            delay = 30
        self.wpcmd.delay(delay)
    def do_endloop(self, args):
        'Stops change loop'
        self.wpcmd.endloop()

    def do_getconf(self, args):
        "Display configuration parameters"
        if len(args) < 1:
            print "Missing parameter" 
        else:
            print "{0}: [{1}]".format(args, self.wpcmd.getconf(args))


    def do_setconf(self, args):
        "name new_value - Sets configuration parameters"
        split_args = args.split(' ')
        if len(split_args) < 2:
            print "Missing parameters" 
        self.wpcmd.setconf(split_args[0], split_args[1])

    def do_exit(self, args):
        'Stops any running loop and ends the CLI'
        self.wpcmd.exit() 
