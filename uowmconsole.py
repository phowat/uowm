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
        'bla bla wp change'
        if len(args):
            split_args = args.split(' ')
        else:
            split_args = []
        self.wpcmd.change(split_args)

    def do_startloop(self, args):
        'bla bla wp startloop'
        print len(args)
        if len(args) > 0:
            split_args = args.split(' ')
        else:
            split_args = []
        self.wpcmd.startloop(split_args)

    def do_endloop(self):
        'bla bla wp endloop'
        self.wpcmd.endloop()

    def do_exit(self):
        'some help text'
        self.wpcmd.exit() 
