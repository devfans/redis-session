#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import UserDict
from tornado.web import RequestHandler
from tornado.options import options
from .model import SessionStore

class Session(UserDict):
    def __int__(self, sessionId):
        self._sessionId = sessionId

    @property
    def key(self):
        return SessionStore(options).key

    @property
    def sessionId(self):
        return self._sessionId
    
    def __getitem__(self, key):
        return self.key.hget(key, sessionId=self.sessionId)

    def __setitem__(self, key, value):
        self.key.hset(key, value, sessionId=self.sessionId)
        self.touch()

    def __delitem__(self, key):
        self.key.hel(key, sessionId=self.sessionId)
        self.touch()

    def __contains__(self, key):
        self.key.hexists(key, sessionId=self.sessionId)

    def touch(self):
        self.key.expire(sessionId=self.sessionId)

    def load(self):
        self.key.hgetall(sessionId=self.sessionId)

    def clear(self):
        self.key.delete(sessionId=self.sessionId)

    def save(self, value):
        self.key.hmset(value, sessionId=self.sessionId)
        self.touch()


class SessionHandler(RequestHandler):
    "Build basic request handlers with session handling"

    @property
    def sessionId(self):
        if not hasattr(self, '_sessionId'):
            cookieKey = self.settings.get('cookie_key', 'session-id')
            sessionId = self.get_secure_cookie(cookieKey)
            #TODO: Check cookie expiration here
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

