# redis-session
Web session implementation with redis store

[![PYPI Version][pypi-image]][pypi-url]
[![Build Status][travis-image]][travis-url]


## Description
Implementated for python3 web frameworks to handle client sessions(Tornado and Flask are supported, other web frameworks to be supported later), using redis hashes to save session data.

+ For controlling expiration of sessions, we are using redis key expiration, and we only control session expiration at server/database side, while using default expiration time of secure cookies for session ids.

+ Reading session data in a request will cause a session expiration reset per request. Modify session data will cause a reset per modification.

+ Please specify `cookie_secret`(`SECRET_KEY` for flask) for we are using secure cookie keys.

+ Getting session attributes is achived by directly fetching from redis to avoid stale data being read. So, when it's not necessary, copy the data instead of reading again, which means:
```
(Example of tornado)
# Do this
name = self.session.name.str
names.append(name)
self.session.name = make_new_name(name)
# Instead of (When we are not worried about conflicts with other processes/threads)
names.append(self.session.name.str)
self.session.name = make_new_name(self.session.name.str)  # This will read name from redis again
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
self.session.name.raw         # b'stefan'

# Parsing to types
self.session.name.str         # Fallback to ''
self.session.count.int        # Fallback to 0
self.session.vip.bool         # Fallback to False
self.session.properties.json  # Fallback to {}

# Check if is none
self.session.age.none
 
```


## Tornado

+ We are using tornado.options module, so please run below once at start.
```
tornado.options.parse_command_line()
# or
tornado.options.parse_config_file("/etc/server.conf")
```
### Command line parameters

```
# For tornado users
define('session-redis', default='redis://localhost:6379', help='session store redis url', type=str)
define('session-redis-prefix', help='redis key prefix', type=str)
define('session-expire', help='session ttl(seconds)', type=int)
define('session-cookie-id', help='cookie key, default: session-id', type=str)
define('session-cookie-secure', default=True, help='if use secure session cookie', type=bool)
define('session-cookie-domain', default='', help='session cookie domain', type=str)
define('session-cookie-path', default='/', help='session cookie path', type=str)
define('session-cookie-http-only', default=True, help='if set session cookie as http only', type=bool)
```

### Example

```
# With tornado framework

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
        self.write(f'Current session value of count:{self.session.count.int}\n')

def main():
    parse_command_line()
    application = tornado.web.Application([(r'/', MainHandler)], cookie_secret='udxas-efasx-ase323fs-3efsxf3eFdes')
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()
```

## Flask

Please note `httpOnly` for flask session cookie is not well implementated in this project yet.

### Example
```
from redis_session.flask_session import setup_session
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def handle():
    count = request.session.count.int
    res = f'Current session value of count:{count}\n'
    request.session.count = count + 1
    res += f'Current session value:{request.session.count.int}\n'
    return res


def main():
    app.config.from_mapping(
        ENV='dev',
        SECRET_KEY='demo',
        SESSION_REDIS='redis://localhost:6379',
        SESSION_REDIS_PREFIX='appName',
        SESSION_COOKIE_ID='app-session-id',
        SESSION_COOKIE_HTTP_ONLY = True,
        SESSION_COOKIE_SECURE = False,
        SESSION_COOKIE_DOMAIN = '.mydomain.com',
        SESSION_COOKIE_PATH = '/',
        SESSION_EXPIRE=60*60*24*7
    )
    setup_session(app)
    app.run(port=3000)

if __name__ == "__main__":
    main()
```

[pypi-image]: https://img.shields.io/pypi/v/redis-session.svg
[pypi-url]: https://pypi.org/project/redis-session/
[travis-image]: https://img.shields.io/travis/devfans/redis-session/master.svg
[travis-url]: https://travis-ci.org/devfans/redis-session
