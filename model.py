#!/usr/bin/env python
# -*- coding: utf-8 -*-
from uuid import uuid4
import redis

class Store(object):
    """Initialiaze redis client"""

    @classmethod
    def initialize(cls, url):
        cls.redisUrl = url
        cls.client = cls.getClient()

    @classmethod
    def getClient(cls):
        pool = redis.ConnectionPool.from_url(cls.redisUrl)
        client = redis.StrictRedis(connection_pool=pool)
        return client

    @classmethod
    def getPipeline(cls, **kwargs):
        transaction = kwargs.get('transaction', True)
        return cls.client.pipeline(transaction=transaction)


class RedisKey(object):
    """General redis key"""

    def __init__(self, **kwargs):
        if 'tpl' not in kwargs:
            raise Exception("Template(tpl) needed for redis keys")
        self._tpl = kwargs['tpl']
        self._expire = kwargs.get('exp', None)

    def _key(self, kwargs):
        return self._tpl.format(**kwargs)

    def ttl(self, **kwargs):
        return Store.client.ttl(self._key(kwargs))

    def expire(self, delta, **kwargs):
        return Store.client.expire(self._key(kwargs), delta)

    def delete(self, **kwargs):
        return Store.client.delete(self._key(kwargs))

    def exist(self, **kwargs):
        return Store.client.exists(self._key(kwargs))


class RedisHash(RedisKey):

    def hset(self, field, value, **kwargs):
        Store.client.hset(self._key(kwargs), field, value)

    def hsetnx(self, field, value, **kwargs):
        return Store.client.hsetnx(self._key(kwargs), field, value)

    def hexists(self, field, **kwargs):
        return Store.client.hset(self._key(kwargs), field)

    def hkeys(self, **kwargs):
        return Store.client.hkeys(self._key(kwargs))

    def hgetall(self, **kwargs):
        return Store.client.hgetall(self._key(kwargs))


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SessionStore(metaclass=Singleton):
    """ We save sessions as hashsets in redis """

    def __init__(self, kwargs):
        Store.initialize(url)
        prefix = kwargs.get('prefix', 'tornado')
        exp = kwargs.get('expire')
        tpl = prefix + ':sessions:{sessionId}'
        self._key = RedisHash(tpl=tpl, exp=exp)

    @property
    def key(self):
        return self._key

    def newSessionId(self):
        return '{}-{}-{}'.format(uuid4(), uuid4(), uuid4())

