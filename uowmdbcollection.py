#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rethinkdb as r

if __name__ == '__main__':
    _conn = r.connect(db='uowm')
    cur = r.table('wallpapers').\
          filter(r.row['tags'].contains("earthporn")).run(_conn)
    for cu in cur:
        print cu
