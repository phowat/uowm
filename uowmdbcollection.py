#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rethinkdb as r
import random


#TODO: 
# Multiple tags and 
# Multiple tags or
# Display new ones( without a last display timestamp) 

if __name__ == '__main__':
    _conn = r.connect(db='uowm')
    cur = r.table('wallpapers').\
          filter(r.row['tags'].contains("earthporn")).run(_conn)
    collection = []
    for cu in cur:
        collection.append(cu)
    print random.choice(collection)
