#!/usr/bin/env python
# -*- coding: utf-8 -*-

from redis_session.flask_session import attach_session
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
        SESSION_HTTP_ONLY = True,
        SESSION_EXPIRE=60*60*24*7
    )
    attach_session(app)
    app.run(port=3000)

if __name__ == "__main__":
    main()
