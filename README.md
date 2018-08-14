# redis-session
Web session implementation with redis store

[![PYPI Version][pypi-image]][pypi-url]
[![Build Status][travis-image]][travis-url]


## Description
Implementated for python3 and tornado(other web frameworks to be supported later), using redis hashes to save session data.

+ For controlling expiration of sessions, we are using redis key expiration, and we only control session expiration at server/database side, while using default expiration time of secure cookies for session ids.

+ Reading session data in a request will cause a session expiration reset per request. Modify session data will cause a reset per modification.

+ We are using tornado.options module, so please run below once at start.
```
tornado.options.parse_command_line()
# or
tornado.options.parse_config_file("/etc/server.conf")
```
+ Please specify `cookie_secret` for we are using secure cookie keys.

+ Getting session attributes is achived by directly fetching from redis to avoid stale data being read. So, when it's not necessary, copy the data instead of reading again, which means:
```
# Do this
name = self.session.name.str
names.append(name)
self.session.name = make_new_name(name)
# Instead of (When we are not worried about conficts with other process)
names.append(self.session.name.str)
self.session.name = make_new_name(self.session.name.str)  # This will read name from redis again
```


## Command line parameters

```
# For tornado users
define('session-redis', default='redis://localhost:6379', help='session store redis url', type=str)
define('session-redis-prefix', help='redis key prefix', type=str)
define('session-expire', help='session ttl(seconds)', type=int)
define('session-cookie-id', help='cookie key, default: session-id', type=str)
```

## Setup & Install

#### Via pip

```
pip install redis_session
```

#### From source

```
python setup.py build && python setup.py install
```

## Session data parsing
We provide common redis result parsing methods. For example:

```
# Get raw bytes
self.session.name.raw

# Parsing to types
self.session.name.str
self.session.count.int
self.session.exist.bool

# Check if is none
self.session.age.none
 
```

## Example

```
# With tornado framework

import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import options, define, parse_command_line
from redis_session import SessionHandler

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
