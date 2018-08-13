#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.httpserver
import tornado.ioloop

from .session import SessionHandler

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', MainHandler),
        ]
        settings = dict(
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(SessionHandler):
    def get(self):
        self.write("Redis Session Example:<br/>")
        if 'sv' in self.session:
            sv = self.session["sv"]
        else:
            sv = 0
        self.write('Current Session Value:%s' % sv)
        self.session['sv'] = sv + 1


def main():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(3000)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
