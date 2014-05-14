#!/usr/bin/env python
# -*- coding: utf-8 -*-

import atexit
import os
import code
import readline
import cmd
from uowmcmd import WPCmd
import sys

class WPConsole(cmd.Cmd):
    def __init__(self, dirs=[]):
        cmd.Cmd.__init__(self)
        self.wpcmd = WPCmd(dirs)

    def do_change(self, args):
        '[dir1 dir2 ...] - Changes current wallpaper once'
        if len(args):
            split_args = args.split(' ')
        else:
            split_args = []
        self.wpcmd.change(split_args)

    def do_startloop(self, args):
        '[interval] - Starts wallpaper change loop every N seconds'
        print len(args)
        if len(args) > 0:
            split_args = args.split(' ')
        else:
            split_args = []
        self.wpcmd.startloop(split_args)

    def do_endloop(self, args):
        'Stops change loop'
        self.wpcmd.endloop()

    def do_exit(self, args):
        'Stops any running loop and ends the CLI'
        self.wpcmd.exit() 
