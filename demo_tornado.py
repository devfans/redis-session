#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import options, define, parse_command_line
from redis_session.tornado_session import SessionHandler

define('port', default=3000, help='run on the given port', type=int)
define('debug', default=False, help='run in debug mode')

class MainHandler(SessionHandler):
    def get(self):
        count = self.session.count.int
        self.write(f'Current session value of count:{count}\n')
        self.session.count = count + 1
        self.write(f'Current session value:{self.session.count.int}\n')

def main():
    parse_command_line()
    application = tornado.web.Application([(r'/', MainHandler)], cookie_secret='udxas-efasx-ase323fs-3efsxf3eFdes')
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
