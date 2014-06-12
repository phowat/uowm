#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rethinkdb as r
from socket import gethostname

class WPCollections(object):
    def __init__(self):
        _conn = r.connect(db='uowm')
        hostname = gethostname()
        cols = r.table('collections').\
               filter(r.row['hostname'] == hostname).run(_conn)

        self.collections = {}
        for col in cols:
            self.collections[col['name']] = col
