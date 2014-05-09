#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rethinkdb as r
import os
from socket import gethostname

class WPConfigurationDB(object):
    def __init__(self):
        _conn = r.connect(db='uowm')
        homedir = os.path.expanduser('~')
        confs = r.table('config').\
               filter(r.row['hostname'] == gethostname()).\
               limit(1).run(_conn)
        # TODO: There's gotta be a better way...
        conf = {}
        for c in confs:
            conf = c
            break

        self.append_default_dirs = conf.get('append_default_dirs', False)
        self.log_file = conf.get('log_file',homedir+"/.uowm/log")
        self.no_repeat = int(conf.get('no_repeat', 20))
        self.backend = conf.get('backend', 'Noop')
        self.cycle_dirs = conf.get('cycle_dirs', False)
