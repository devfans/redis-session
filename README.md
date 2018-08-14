# redis-session
Web session implementation with redis store

[![PYPI Version][pypi-image]][pypi-url]
[![Build Status][travis-image]][travis-url]


## Description
Implementated for python3 and tornado(other web framewors to be supported later), using redis hashes to save session data.

+ For control expiration of sessions, we are using redis key expiration, and we only control session expiration at server/database side, using default expiration time of secure cookie for session id

+ We are using tornado.options module, so please run below once at starting
```
tornado.options.parse_command_line()
# or
tornado.options.parse_config_file("/etc/server.conf")
```
+ Please specify `cookie_secret` for we are using secure cookie key


## Command line parameters

```
# For tornado users
define('session-redis', default='redis://localhost:6379', help='session store redis url', type=str)
define('session-redis-prefix', help='redis key prefix', type=str)
define('session-expire', help='session ttl(seconds)', type=int)
define('session-cookie-id', help='cookie key, default: session-id', type=str)
```

## Setup & Install

```
# Via pip
pip install redis_session

# From source
python setup.py build && python setup.py install
```

## Example

```
# With tornado framework

import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import options, define, parse_command_line
from tornado_redis_session import SessionHandler

define('port', default=3000, help='run on the given port', type=int)
define('debug', default=False, help='run in debug mode')

class MainHandler(SessionHandler):
    def get(self):
        self.write('Redis Session Example\n')
        count = self.session.count.int
        self.write(f'Current Session Value:{count}\n')
        self.session.count = count + 1
        self.write(f'Current Session Value:{self.session.count.int}\n')

def main():
    parse_command_line()
    application = tornado.web.Application([(r'/', MainHandler)], cookie_secret='udxas-efasx-ase323fs-3efsxf3eFdes')
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
```

[pypi-image]: https://img.shields.io/pypi/v/redis-session.svg
[pypi-url]: https://pypi.org/project/redis-session/
[travis-image]: https://img.shields.io/travis/devfans/redis-session/master.svg
[travis-url]: https://travis-ci.org/devfans/redis-session
