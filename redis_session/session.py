#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from tornado.web import RequestHandler
from tornado.options import options, define
from redis_session.model import SessionStore

define('session-redis', default='redis://localhost:6379', help='session store redis url', type=str)
define('session-redis-prefix', help='redis key prefix', type=str)
define('session-expire', help='session ttl(seconds)', type=int)
define('session-cookie-id', help='cookie key, default: session-id', type=str)

class RedisResult(object):
    """Redis result parser"""

    def __init__(self, raw):
        self.raw = raw

    @property
    def int(self):
        try:
            return int(self.raw)
        except:
            return 0

    @property
    def bool(self):
        return self.str == 'True'

    @property
    def str(self):
        return '' if self.none else self.raw.decode('utf8')

    @property
    def none(self):
        return self.raw is None

    @property
    def json(self):
        try:
            return json.loads(self.raw)
        except:
            return {}

class Session(object):
    def __init__(self, sessionId):
        super(Session, self).__init__()
        object.__setattr__(self, '_sessionId', sessionId)
        object.__setattr__(self, '_key', SessionStore(options).key)
        self.touch()

    @property
    def key(self):
        return self._key

    @property
    def sessionId(self):
        return self._sessionId
    
    def __getattr__(self, key):
        return RedisResult(self.key.hget(key, sessionId=self.sessionId))

    def __setattr__(self, key, value):
        self.key.hset(key, value, sessionId=self.sessionId)
        self.touch()

    def __delattr__(self, key):
        self.key.hel(key, sessionId=self.sessionId)

    def __hasattr__(self, key):
        self.key.hexists(key, sessionId=self.sessionId)

    def touch(self):
        self.key.expire(sessionId=self.sessionId)

    def load(self):
        return self.key.hgetall(sessionId=self.sessionId)

    def clear(self):
        self.key.delete(sessionId=self.sessionId)

    def save(self, value):
        self.key.hmset(value, sessionId=self.sessionId)
        self.touch()


class SessionHandler(RequestHandler):
    """Build basic request handlers with session handling"""

    @property
    def sessionId(self):
        if not hasattr(self, '_sessionId'):
            cookieKey = options.session_cookie_id or 'session-id'
            sessionId = self.get_secure_cookie(cookieKey)
            if isinstance(sessionId, bytes):
                sessionId = sessionId.decode('utf8')
            if sessionId is None or sessionId == '':
                sessionId = SessionStore.newSessionId()
                self.set_secure_cookie(cookieKey, sessionId)
            self._sessionId = sessionId
        return self._sessionId

    @property
    def session(self):
        if not hasattr(self, '_session'):
            self._session = Session(self.sessionId)
        return self._session

    @session.setter
    def session(self, value):
        self.session.save(value)

    @session.deleter
    def session(self):
        self.session.clear()

