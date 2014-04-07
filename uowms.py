#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.ioloop
import tornado.web
from uowmlib import change_wallpaper

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

class ChangeWPHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'response': 0}
        change_wallpaper()
        self.write(response)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/change_wallpaper", ChangeWPHandler),
])

def main():
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main();
